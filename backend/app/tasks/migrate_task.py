"""Celery task for PQC migration."""

import hashlib
import random
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select

from app.celery_app import celery_app
from app.core.database import SyncSessionLocal
from app.models.audit_log import AuditLog
from app.models.endpoint import Endpoint
from app.models.migration_config import MigrationConfig
from app.models.scan_job import ScanJob
from app.pqc.config_generator import generate_migration_configs
from app.pqc.operations import demo_ml_dsa_65, demo_ml_kem_768


# Tier priority for sorting
TIER_PRIORITY = {
    'critical': 4,
    'high': 3,
    'medium': 2,
    'low': 1,
    'unknown': 0,
}


@celery_app.task(bind=True, name='fortiq.run_migration')
def run_migration_task(self, job_id: str, endpoint_ids: list[str] = None) -> dict:
    """Run PQC migration for specified endpoints.

    This is a SYNC task running in a Celery worker or in-process.

    Args:
        self: Bound Celery task or None
        job_id: UUID of the ScanJob or list of endpoint IDs if self is job_id
        endpoint_ids: List of endpoint UUIDs to migrate

    Returns:
        dict: Task result summary
    """
    if endpoint_ids is None:
        endpoint_ids = job_id
        job_id = self
        self = None

    session = SyncSessionLocal()

    try:
        # Load job
        job = session.execute(
            select(ScanJob).where(ScanJob.id == UUID(job_id))
        ).scalar_one()

        # Update job status
        job.status = 'running'
        job.started_at = datetime.now(timezone.utc)
        session.commit()

        # Get endpoints, sort by priority
        endpoints = session.execute(
            select(Endpoint).where(Endpoint.id.in_([UUID(eid) for eid in endpoint_ids]))
        ).scalars().all()

        # Sort: critical first, then by risk_score DESC
        endpoints_sorted = sorted(
            endpoints,
            key=lambda ep: (TIER_PRIORITY.get(ep.risk_tier, 0), ep.risk_score or 0),
            reverse=True
        )

        job.total = len(endpoints_sorted)
        session.commit()

        # Migrate each endpoint
        for i, endpoint in enumerate(endpoints_sorted):
            # Update status
            endpoint.migration_status = 'in_progress'
            session.commit()

            # Audit: migration started
            _write_audit(
                session, endpoint, 'migration_started',
                old_value='pending', new_value='in_progress',
                detail={'algorithm': endpoint.algorithm}
            )

            # Run PQC demos
            kem_result = demo_ml_kem_768()
            sig_result = demo_ml_dsa_65()

            # Generate and save configs
            configs = generate_migration_configs(endpoint)
            for config_text in configs:
                config = MigrationConfig(
                    endpoint_id=endpoint.id,
                    config_type='pqc_migration',
                    config_text=config_text,
                )
                session.add(config)

            # Audit: configs generated
            _write_audit(
                session, endpoint, 'configs_generated',
                old_value=None, new_value=f'{len(configs)} configs',
                detail={'config_count': len(configs)}
            )

            # Transition to hybrid mode
            endpoint.migration_status = 'hybrid'
            _write_audit(
                session, endpoint, 'hybrid_mode_enabled',
                old_value='in_progress', new_value='hybrid',
                detail={'kem': kem_result, 'sig': sig_result}
            )
            session.commit()

            # Deterministic pass/fail (80% pass rate)
            seed = hashlib.md5(str(endpoint.id).encode()).hexdigest()[:8]
            rng = random.Random(seed)
            passes = rng.random() < 0.80

            if passes:
                # Success
                endpoint.migration_status = 'complete'
                endpoint.migrated_algorithm = 'ML-KEM-768 + ML-DSA-65'
                _write_audit(
                    session, endpoint, 'migration_complete',
                    old_value='hybrid', new_value='complete',
                    detail={'algorithm': 'ML-KEM-768 + ML-DSA-65'}
                )
            else:
                # Rollback
                endpoint.migration_status = 'rollback'
                _write_audit(
                    session, endpoint, 'migration_rollback',
                    old_value='hybrid', new_value='rollback',
                    detail={'reason': 'Hybrid validation timeout (simulated)', 'original_algorithm': endpoint.algorithm}
                )

            # Update progress
            job.processed = i + 1
            session.commit()

            # Update task state
            if self and hasattr(self, 'update_state'):
                self.update_state(
                    state='PROGRESS',
                    meta={
                        'processed': i + 1,
                        'total': job.total,
                        'current': endpoint.name,
                    }
                )

        # Complete job
        job.status = 'completed'
        job.completed_at = datetime.now(timezone.utc)
        session.commit()

        return {
            'status': 'completed',
            'processed': len(endpoints_sorted),
            'job_id': job_id,
        }

    except Exception as e:
        if session:
            job = session.execute(
                select(ScanJob).where(ScanJob.id == UUID(job_id))
            ).scalar_one_or_none()
            if job:
                job.status = 'failed'
                job.error = str(e)
                session.commit()
        raise
    finally:
        session.close()


def _write_audit(
    session,
    endpoint: Endpoint,
    action: str,
    old_value: str,
    new_value: str,
    detail: dict | None = None
) -> None:
    """Write audit log entry."""
    audit = AuditLog(
        entity_type='endpoint',
        entity_id=endpoint.id,
        action=action,
        old_value=old_value,
        new_value=new_value,
        detail=detail,
    )
    session.add(audit)
