"""Celery task for endpoint classification."""

from datetime import datetime, timezone
from pathlib import Path
from uuid import UUID

from sqlalchemy import select

from app.celery_app import celery_app
from app.core.config import settings
from app.core.database import SyncSessionLocal
from app.models.endpoint import Endpoint
from app.models.scan_job import ScanJob
from app.qml.features import FeatureNormalizer, endpoint_to_features
from app.qml.vqc import VQCClassifier


# Resolve model paths relative to backend directory
_backend_dir = Path(__file__).resolve().parent.parent.parent


def _get_model_path(relative_path: str) -> Path:
    """Get absolute path for model file."""
    return _backend_dir / relative_path


@celery_app.task(bind=True, name='fortiq.classify_endpoints')
def classify_endpoints_task(self, job_id: str = None) -> dict:
    """Classify all endpoints using trained VQC model.

    This is a SYNC task running in a Celery worker or in-process.

    Args:
        self: Bound Celery task or None
        job_id: UUID of the ScanJob

    Returns:
        dict: Task result summary
    """
    if job_id is None:
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

        # Check if model files exist
        vqc_path = _get_model_path(settings.VQC_PARAMS_PATH)
        normalizer_path = _get_model_path(settings.NORMALIZER_PATH)

        if not vqc_path.exists() or not normalizer_path.exists():
            job.status = 'failed'
            job.error = "Models not trained. Run 'python scripts/train_models.py' first."
            job.completed_at = datetime.now(timezone.utc)
            session.commit()
            return {
                'status': 'failed',
                'error': job.error,
                'job_id': job_id,
            }

        # Load model and normalizer
        vqc = VQCClassifier.load(str(vqc_path))
        normalizer = FeatureNormalizer.load(str(normalizer_path))

        # Get all endpoints (reclassify all for now)
        endpoints = session.execute(select(Endpoint)).scalars().all()

        job.total = len(endpoints)
        session.commit()

        # Classify each endpoint
        for i, endpoint in enumerate(endpoints):
            # Extract and normalize features
            features = endpoint_to_features(endpoint)
            features_norm = normalizer.transform([features])[0]

            # Predict tier and score
            tier = vqc.predict([features_norm])[0]
            proba = vqc.predict_proba([features_norm])[0]
            score = float(proba.max())

            # Update endpoint
            endpoint.risk_tier = tier
            endpoint.risk_score = score
            endpoint.last_scanned_at = datetime.now(timezone.utc)

            # Commit every 10 endpoints
            if (i + 1) % 10 == 0:
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

        # Final commit
        job.processed = len(endpoints)
        job.status = 'completed'
        job.completed_at = datetime.now(timezone.utc)
        session.commit()

        return {
            'status': 'completed',
            'processed': len(endpoints),
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

