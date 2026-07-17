"""Job Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class JobCreate(BaseModel):
    """Request schema for creating a job."""

    pass  # No input needed for classification


class JobStatus(BaseModel):
    """Job status response."""

    id: UUID
    status: str  # pending|running|completed|failed
    job_type: str  # classify|migrate
    total: int
    processed: int
    progress_pct: float  # processed / total * 100, rounded 1 decimal
    current_endpoint: str | None = None  # name of endpoint being processed
    started_at: datetime | None
    completed_at: datetime | None
    error: str | None

    model_config = {"from_attributes": True}
