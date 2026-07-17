"""Endpoint model - the core asset registry entity."""

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Float, Index, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class Endpoint(Base, UUIDMixin, TimestampMixin):
    """
    Endpoint entity representing a cryptographic service or asset.

    This is the atomic unit of the Fortiq system - an API gateway,
    database connection, IoT device, firmware system, or web server.
    """

    __tablename__ = "endpoints"

    # Identity
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    host: Mapped[str] = mapped_column(String(255), nullable=False)
    port: Mapped[int] = mapped_column(Integer, nullable=False)

    # Classification
    endpoint_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # api|database|iot|firmware|web

    # Cryptography
    algorithm: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # RSA-2048|RSA-4096|ECC-256|ECC-384
    key_length: Mapped[int] = mapped_column(Integer, nullable=False)

    # Risk factors
    data_sensitivity: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # 1-5, 5 = most sensitive
    exposure_surface: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # internet-facing|internal|air-gapped
    traffic_volume: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # low|medium|high|critical
    cert_expiry_days: Mapped[int] = mapped_column(
        Integer, nullable=False
    )  # negative = expired

    # VQC classification output
    risk_tier: Mapped[str] = mapped_column(
        String(20), nullable=False, default="unknown"
    )  # critical|high|medium|low|unknown
    risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Migration state
    migration_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )  # pending|in_progress|hybrid|complete|rollback
    migrated_algorithm: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Timestamps
    last_scanned_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    __table_args__ = (
        Index("idx_endpoints_risk_tier", "risk_tier"),
        Index("idx_endpoints_migration_status", "migration_status"),
        Index("idx_endpoints_algorithm", "algorithm"),
    )

    def __repr__(self) -> str:
        return f"<Endpoint {self.name} ({self.risk_tier})>"
