from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class MigrationConfig(Base, UUIDMixin):
    """
    MigrationConfig entity storing generated configuration files.

    Config types: ml_kem_768_kem|ml_dsa_65_sig|nginx_tls|openssl_conf|yaml_plan
    """

    __tablename__ = "migration_configs"

    endpoint_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("endpoints.id", ondelete="CASCADE"),
        nullable=False,
    )
    config_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # ml_kem_768_kem|ml_dsa_65_sig|nginx_tls|openssl_conf|yaml_plan
    config_text: Mapped[str] = mapped_column(Text, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


    __table_args__ = (Index("idx_migration_configs_endpoint", "endpoint_id"),)

    def __repr__(self) -> str:
        return f"<MigrationConfig {self.config_type} for {self.endpoint_id}>"
