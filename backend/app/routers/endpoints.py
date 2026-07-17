"""Endpoints API routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.dependencies import CurrentUser, DbSession
from app.repositories.migration_repository import MigrationRepository
from app.schemas.common import PaginationMeta, ResponseEnvelope, ok
from app.schemas.endpoint import DashboardStats, EndpointDetail, EndpointFilters, EndpointListItem
from app.schemas.migration import MigrationConfigDTO
from app.services.endpoint_service import EndpointService

router = APIRouter()


@router.get("", response_model=ResponseEnvelope[list[EndpointListItem]])
async def list_endpoints(
    db: DbSession,
    user: CurrentUser,
    tier: str | None = Query(None, description="Filter by risk tier"),
    status: str | None = Query(None, description="Filter by migration status"),
    algorithm: str | None = Query(None, description="Filter by algorithm"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
):
    """Get paginated list of endpoints with optional filters."""
    filters = EndpointFilters(
        tier=tier,
        status=status,
        algorithm=algorithm,
        page=page,
        per_page=per_page,
    )
    service = EndpointService(db)
    items, meta = await service.list_endpoints(filters)
    return ok(items, meta)


@router.get("/stats/dashboard", response_model=ResponseEnvelope[DashboardStats])
async def get_dashboard_stats(
    db: DbSession,
    user: CurrentUser,
):
    """Get aggregate statistics for the dashboard."""
    service = EndpointService(db)
    stats = await service.get_dashboard_stats()
    return ok(stats)


@router.get("/{endpoint_id}", response_model=ResponseEnvelope[EndpointDetail])
async def get_endpoint(
    endpoint_id: UUID,
    db: DbSession,
    user: CurrentUser,
):
    """Get full endpoint detail by ID."""
    service = EndpointService(db)
    endpoint = await service.get_endpoint(endpoint_id)
    if not endpoint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Endpoint not found",
        )
    return ok(endpoint)


@router.get("/{endpoint_id}/migration-config", response_model=ResponseEnvelope[list[MigrationConfigDTO]])
async def get_migration_configs(
    endpoint_id: UUID,
    db: DbSession,
    user: CurrentUser,
):
    """Get migration configs for an endpoint."""
    repo = MigrationRepository(db)
    configs = await repo.get_configs_by_endpoint(endpoint_id)
    items = [MigrationConfigDTO.model_validate(c) for c in configs]
    return ok(items)
