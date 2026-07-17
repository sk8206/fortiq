from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class ScanJob(Base, UUIDMixin):
    """
    ScanJob entity tracking async classification and migration tasks.

    Status: pending|running|completed|failed
    Job type: classify|migrate
    """

    __tablename__ = "scan_jobs"

    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )  # pending|running|completed|failed
    job_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # classify|migrate

    total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    processed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


    def __repr__(self) -> str:
        return f"<ScanJob {self.id} ({self.job_type}: {self.status})>"

    @property
    def progress_pct(self) -> float:
        """Calculate progress percentage."""
        if self.total == 0:
            return 0.0
        return round((self.processed / self.total) * 100, 1)
