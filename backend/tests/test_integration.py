"""Integration tests for Phase 2 & 3."""

import time
import pytest
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.endpoint import Endpoint
from app.models.scan_job import ScanJob
from app.models.model_evaluation import ModelEvaluation
from app.models.audit_log import AuditLog
from app.tasks.classify_task import classify_endpoints_task
from app.tasks.migrate_task import run_migration_task


@pytest.fixture(autouse=True)
async def seed_integration_data(db_session):
    """Seed default database records for integration tests."""
    from app.core.security import get_password_hash
    from app.models.user import User
    import random

    # Add admin user
    admin = User(username="admin", hashed_password=get_password_hash("fortiq-demo-2024"))
    db_session.add(admin)

    # Add model evaluations
    db_session.add(ModelEvaluation(
        model_type="vqc", binary_class="all",
        accuracy=0.85, precision_score=0.86,
        recall=0.85, f1_score=0.85,
        training_samples=80, test_samples=20,
    ))
    db_session.add(ModelEvaluation(
        model_type="svm", binary_class="all",
        accuracy=0.80, precision_score=0.81,
        recall=0.80, f1_score=0.80,
        training_samples=80, test_samples=20,
    ))

    # Add 100 endpoints
    random.seed(42)
    endpoint_types = ["api", "database", "iot", "firmware", "web"]
    algorithms = ["RSA-2048", "RSA-4096", "ECC-256", "ECC-384"]
    key_lengths = {"RSA-2048": 2048, "RSA-4096": 4096, "ECC-256": 256, "ECC-384": 384}
    exposures = ["internet-facing", "internal", "air-gapped"]
    traffics = ["low", "medium", "high", "critical"]

    for i in range(100):
        ep_type = random.choice(endpoint_types)
        algo = random.choice(algorithms)
        exp = random.choice(exposures)
        traf = random.choice(traffics)
        port = 8080 + i
        data_sens = random.randint(1, 5)
        cert_expiry = random.randint(10, 365)
        
        ep = Endpoint(
            name=f"ep-{i}",
            host=f"10.0.0.{i}",
            port=port,
            endpoint_type=ep_type,
            algorithm=algo,
            key_length=key_lengths[algo],
            data_sensitivity=data_sens,
            exposure_surface=exp,
            traffic_volume=traf,
            cert_expiry_days=cert_expiry,
            risk_tier="high" if i < 10 else "low",
            risk_score=0.8 if i < 10 else 0.2,
            migration_status="pending",
        )
        db_session.add(ep)

    await db_session.commit()



@pytest.mark.asyncio
async def test_classification_integration():
    """Test classification task updates endpoints."""
    async with AsyncSessionLocal() as session:
        # Create a test job
        job = ScanJob(job_type='classify', total=100, status='pending')
        session.add(job)
        await session.commit()
        await session.refresh(job)

        # Run classification (sync)
        classify_endpoints_task(str(job.id))

        # Wait a moment
        time.sleep(1)

        # Verify job completed
        await session.refresh(job)
        assert job.status == 'completed'
        assert job.processed == 100

        # Verify endpoints updated
        result = await session.execute(
            select(Endpoint).where(Endpoint.risk_tier != 'unknown')
        )
        classified = result.scalars().all()
        assert len(classified) > 0


@pytest.mark.asyncio
async def test_migration_integration():
    """Test migration task creates audit logs."""
    async with AsyncSessionLocal() as session:
        # Get some high-risk endpoints
        result = await session.execute(
            select(Endpoint.id).where(Endpoint.risk_tier == 'high').limit(5)
        )
        endpoint_ids = [str(row[0]) for row in result.all()]

        # Create job
        job = ScanJob(job_type='migrate', total=len(endpoint_ids), status='pending')
        session.add(job)
        await session.commit()
        await session.refresh(job)

        # Run migration (sync)
        run_migration_task(str(job.id), endpoint_ids)

        # Wait a moment
        time.sleep(1)

        # Verify job completed
        await session.refresh(job)
        assert job.status == 'completed'
        assert job.processed == len(endpoint_ids)

        # Verify audit logs created
        result = await session.execute(select(AuditLog))
        logs = result.scalars().all()
        assert len(logs) >= len(endpoint_ids) * 4  # At least 4 logs per endpoint


@pytest.mark.asyncio
async def test_model_evaluations_exist():
    """Test model evaluations were stored."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(ModelEvaluation))
        evaluations = result.scalars().all()

        assert len(evaluations) >= 2
        model_names = [e.model_type for e in evaluations]
        assert 'vqc' in model_names
        assert 'svm' in model_names
