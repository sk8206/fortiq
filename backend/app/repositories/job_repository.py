"""Job repository for database access."""

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.scan_job import ScanJob


class JobRepository:
    """Repository for ScanJob entity database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, job_type: str, total: int = 0) -> ScanJob:
        """Create a new job."""
        job = ScanJob(
            job_type=job_type,
            status="pending",
            total=total,
            processed=0,
        )
        self.db.add(job)
        await self.db.flush()
        return job

    async def get_by_id(self, job_id: UUID) -> ScanJob | None:
        """Get a job by ID."""
        result = await self.db.execute(
            select(ScanJob).where(ScanJob.id == job_id)
        )
        return result.scalar_one_or_none()

    async def update_status(
        self,
        job_id: UUID,
        status: str,
        processed: int | None = None,
        error: str | None = None,
    ) -> ScanJob | None:
        """Update job status."""
        job = await self.get_by_id(job_id)
        if job:
            job.status = status
            if processed is not None:
                job.processed = processed
            if error is not None:
                job.error = error
            if status == "running" and job.started_at is None:
                job.started_at = datetime.now(timezone.utc)
            if status in ("completed", "failed"):
                job.completed_at = datetime.now(timezone.utc)
            await self.db.flush()
        return job
