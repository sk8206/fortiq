"""Migration repository for database access."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.models.migration_config import MigrationConfig
from app.schemas.migration import AuditLogFilters


class MigrationRepository:
    """Repository for migration-related database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_config(
        self, endpoint_id: UUID, config_type: str, config_text: str
    ) -> MigrationConfig:
        """Create a migration config record."""
        config = MigrationConfig(
            endpoint_id=endpoint_id,
            config_type=config_type,
            config_text=config_text,
        )
        self.db.add(config)
        await self.db.flush()
        return config

    async def get_configs_by_endpoint(self, endpoint_id: UUID) -> list[MigrationConfig]:
        """Get all migration configs for an endpoint."""
        result = await self.db.execute(
            select(MigrationConfig)
            .where(MigrationConfig.endpoint_id == endpoint_id)
            .order_by(MigrationConfig.generated_at.desc())
        )
        return list(result.scalars().all())


class AuditRepository:
    """Repository for audit log database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        action: str,
        entity_type: str,
        entity_id: UUID,
        old_value: str | None = None,
        new_value: str | None = None,
        detail: dict | None = None,
    ) -> AuditLog:
        """Create an audit log entry."""
        entry = AuditLog(
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            old_value=old_value,
            new_value=new_value,
            detail=detail,
        )
        self.db.add(entry)
        await self.db.flush()
        return entry

    async def get_all(
        self, filters: AuditLogFilters
    ) -> tuple[list[AuditLog], int]:
        """Get paginated audit log entries."""
        query = select(AuditLog)

        if filters.endpoint_id:
            query = query.where(
                AuditLog.entity_type == "endpoint",
                AuditLog.entity_id == filters.endpoint_id,
            )

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # Apply pagination and ordering
        offset = (filters.page - 1) * filters.per_page
        query = (
            query.order_by(AuditLog.created_at.desc())
            .offset(offset)
            .limit(filters.per_page)
        )

        result = await self.db.execute(query)
        entries = list(result.scalars().all())

        return entries, total
