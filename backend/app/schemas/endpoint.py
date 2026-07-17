"""Endpoint Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class EndpointBase(BaseModel):
    """Base endpoint fields."""

    name: str = Field(..., min_length=3, max_length=80)
    host: str
    port: int = Field(..., ge=1, le=65535)
    endpoint_type: str  # api|database|iot|firmware|web
    algorithm: str  # RSA-2048|RSA-4096|ECC-256|ECC-384
    key_length: int
    data_sensitivity: int = Field(..., ge=1, le=5)
    exposure_surface: str  # internet-facing|internal|air-gapped
    traffic_volume: str  # low|medium|high|critical
    cert_expiry_days: int


class EndpointListItem(BaseModel):
    """Endpoint summary for list views."""

    id: UUID
    name: str
    host: str
    algorithm: str
    risk_tier: str
    risk_score: float | None
    migration_status: str
    endpoint_type: str
    data_sensitivity: int
    exposure_surface: str
    traffic_volume: str

    model_config = {"from_attributes": True}


class EndpointDetail(EndpointListItem):
    """Full endpoint detail view."""

    port: int
    key_length: int
    cert_expiry_days: int
    migrated_algorithm: str | None
    last_scanned_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EndpointFilters(BaseModel):
    """Query filters for endpoint listing."""

    tier: str | None = None
    status: str | None = None
    algorithm: str | None = None
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=20, ge=1, le=100)


class DashboardStats(BaseModel):
    """Dashboard aggregate statistics."""

    total: int
    by_tier: dict[str, int]  # {"critical": 15, "high": 30, ...}
    by_status: dict[str, int]  # {"pending": 60, "complete": 25, ...}
    compliance_score: float  # 0.0 to 100.0 (one decimal)
