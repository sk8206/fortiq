"""Migration Pydantic schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MigrateRequest(BaseModel):
    """Request schema for migration."""

    endpoint_ids: list[UUID] | None = None
    tier: str | None = None  # "critical"|"high"|"medium"|"low"


class MigrationConfigDTO(BaseModel):
    """Migration config response."""

    id: UUID
    endpoint_id: UUID
    config_type: str
    config_text: str
    generated_at: datetime

    model_config = {"from_attributes": True}


class KEMResult(BaseModel):
    """ML-KEM-768 demo result."""

    algorithm: str  # "ML-KEM-768"
    fips_standard: str  # "FIPS 203"
    nist_security_level: int
    public_key_bytes: int
    ciphertext_bytes: int
    shared_secret_bytes: int
    encapsulation_ok: bool
    decapsulation_ok: bool


class SignatureResult(BaseModel):
    """ML-DSA-65 demo result."""

    algorithm: str  # "ML-DSA-65"
    fips_standard: str  # "FIPS 204"
    nist_security_level: int
    public_key_bytes: int
    signature_bytes: int
    verification_passed: bool


class PQCDemoResult(BaseModel):
    """Combined PQC demo result."""

    ml_kem_768: KEMResult
    ml_dsa_65: SignatureResult


class AuditLogEntry(BaseModel):
    """Audit log entry response."""

    id: UUID
    action: str
    entity_type: str
    entity_id: UUID
    old_value: str | None
    new_value: str | None
    detail: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}


class AuditLogFilters(BaseModel):
    """Query filters for audit log."""

    endpoint_id: UUID | None = None
    page: int = 1
    per_page: int = 20
