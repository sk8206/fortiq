"""Endpoint repository for database access."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.endpoint import Endpoint
from app.schemas.endpoint import DashboardStats, EndpointFilters


class EndpointRepository:
    """Repository for Endpoint entity database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self, filters: EndpointFilters
    ) -> tuple[list[Endpoint], int]:
        """
        Get paginated list of endpoints with optional filters.

        Returns: (list of endpoints, total count)
        """
        query = select(Endpoint)

        # Apply filters
        if filters.tier:
            query = query.where(Endpoint.risk_tier == filters.tier)
        if filters.status:
            query = query.where(Endpoint.migration_status == filters.status)
        if filters.algorithm:
            query = query.where(Endpoint.algorithm == filters.algorithm)

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        # Apply pagination
        offset = (filters.page - 1) * filters.per_page
        query = query.offset(offset).limit(filters.per_page)

        # Order by risk_score descending (highest risk first)
        query = query.order_by(Endpoint.risk_score.desc().nullslast())

        result = await self.db.execute(query)
        endpoints = list(result.scalars().all())

        return endpoints, total

    async def get_by_id(self, endpoint_id: UUID) -> Endpoint | None:
        """Get a single endpoint by ID."""
        result = await self.db.execute(
            select(Endpoint).where(Endpoint.id == endpoint_id)
        )
        return result.scalar_one_or_none()

    async def update_risk(
        self, endpoint_id: UUID, tier: str, score: float
    ) -> Endpoint | None:
        """Update endpoint risk classification."""
        endpoint = await self.get_by_id(endpoint_id)
        if endpoint:
            endpoint.risk_tier = tier
            endpoint.risk_score = score
            await self.db.flush()
        return endpoint

    async def update_migration_status(
        self, endpoint_id: UUID, status: str, algorithm: str | None = None
    ) -> Endpoint | None:
        """Update endpoint migration status."""
        endpoint = await self.get_by_id(endpoint_id)
        if endpoint:
            endpoint.migration_status = status
            if algorithm:
                endpoint.migrated_algorithm = algorithm
            await self.db.flush()
        return endpoint

    async def get_dashboard_stats(self) -> DashboardStats:
        """Get aggregate statistics for the dashboard."""
        # Total count
        total_result = await self.db.execute(select(func.count(Endpoint.id)))
        total = total_result.scalar() or 0

        # Count by tier
        tier_query = select(
            Endpoint.risk_tier, func.count(Endpoint.id)
        ).group_by(Endpoint.risk_tier)
        tier_result = await self.db.execute(tier_query)
        by_tier = {row[0]: row[1] for row in tier_result.all()}

        # Count by status
        status_query = select(
            Endpoint.migration_status, func.count(Endpoint.id)
        ).group_by(Endpoint.migration_status)
        status_result = await self.db.execute(status_query)
        by_status = {row[0]: row[1] for row in status_result.all()}

        # Compliance score: (complete / total) * 100
        complete_count = by_status.get("complete", 0)
        compliance_score = round((complete_count / total) * 100, 1) if total > 0 else 0.0

        return DashboardStats(
            total=total,
            by_tier=by_tier,
            by_status=by_status,
            compliance_score=compliance_score,
        )

    async def get_by_tier(self, tier: str) -> list[Endpoint]:
        """Get all endpoints with a specific risk tier."""
        result = await self.db.execute(
            select(Endpoint)
            .where(Endpoint.risk_tier == tier)
            .order_by(Endpoint.risk_score.desc().nullslast())
        )
        return list(result.scalars().all())

    async def get_by_ids(self, endpoint_ids: list[UUID]) -> list[Endpoint]:
        """Get endpoints by list of IDs."""
        result = await self.db.execute(
            select(Endpoint).where(Endpoint.id.in_(endpoint_ids))
        )
        return list(result.scalars().all())
