"""Endpoint service for business logic."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.endpoint_repository import EndpointRepository
from app.schemas.common import PaginationMeta
from app.schemas.endpoint import (
    DashboardStats,
    EndpointDetail,
    EndpointFilters,
    EndpointListItem,
)


class EndpointService:
    """Service for endpoint-related business logic."""

    def __init__(self, db: AsyncSession):
        self.repo = EndpointRepository(db)

    async def list_endpoints(
        self, filters: EndpointFilters
    ) -> tuple[list[EndpointListItem], PaginationMeta]:
        """Get paginated list of endpoints."""
        endpoints, total = await self.repo.get_all(filters)

        total_pages = (total + filters.per_page - 1) // filters.per_page
        meta = PaginationMeta(
            total=total,
            page=filters.page,
            per_page=filters.per_page,
            total_pages=total_pages,
        )

        items = [EndpointListItem.model_validate(ep) for ep in endpoints]
        return items, meta

    async def get_endpoint(self, endpoint_id: UUID) -> EndpointDetail | None:
        """Get endpoint detail by ID."""
        endpoint = await self.repo.get_by_id(endpoint_id)
        if endpoint:
            return EndpointDetail.model_validate(endpoint)
        return None

    async def get_dashboard_stats(self) -> DashboardStats:
        """Get dashboard statistics."""
        return await self.repo.get_dashboard_stats()
