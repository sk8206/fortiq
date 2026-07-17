"""Tests for endpoint repository."""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.endpoint import Endpoint
from app.repositories.endpoint_repository import EndpointRepository
from app.schemas.endpoint import EndpointFilters


@pytest_asyncio.fixture
async def sample_endpoints(db_session: AsyncSession) -> list[Endpoint]:
    """Create sample endpoints for testing."""
    endpoints = [
        Endpoint(
            name=f"test-endpoint-{i}",
            host=f"10.0.0.{i}",
            port=8080 + i,
            endpoint_type="api",
            algorithm="RSA-2048",
            key_length=2048,
            data_sensitivity=3,
            exposure_surface="internet-facing",
            traffic_volume="medium",
            cert_expiry_days=365,
            risk_tier=["critical", "high", "medium", "low"][i % 4],
            risk_score=0.8 - (i * 0.1),
            migration_status="pending",
        )
        for i in range(10)
    ]
    for ep in endpoints:
        db_session.add(ep)
    await db_session.commit()
    return endpoints


@pytest.mark.asyncio
async def test_get_all_endpoints(db_session: AsyncSession, sample_endpoints: list[Endpoint]):
    """Test getting all endpoints with pagination."""
    repo = EndpointRepository(db_session)
    filters = EndpointFilters(page=1, per_page=5)

    endpoints, total = await repo.get_all(filters)

    assert total == 10
    assert len(endpoints) == 5


@pytest.mark.asyncio
async def test_get_endpoints_by_tier(db_session: AsyncSession, sample_endpoints: list[Endpoint]):
    """Test filtering endpoints by tier."""
    repo = EndpointRepository(db_session)
    filters = EndpointFilters(tier="critical", page=1, per_page=20)

    endpoints, total = await repo.get_all(filters)

    assert all(ep.risk_tier == "critical" for ep in endpoints)


@pytest.mark.asyncio
async def test_get_endpoint_by_id(db_session: AsyncSession, sample_endpoints: list[Endpoint]):
    """Test getting a single endpoint by ID."""
    repo = EndpointRepository(db_session)
    target_id = sample_endpoints[0].id

    endpoint = await repo.get_by_id(target_id)

    assert endpoint is not None
    assert endpoint.id == target_id


@pytest.mark.asyncio
async def test_get_dashboard_stats(db_session: AsyncSession, sample_endpoints: list[Endpoint]):
    """Test getting dashboard statistics."""
    repo = EndpointRepository(db_session)

    stats = await repo.get_dashboard_stats()

    assert stats.total == 10
    assert "critical" in stats.by_tier
    assert "pending" in stats.by_status
    assert 0.0 <= stats.compliance_score <= 100.0


@pytest.mark.asyncio
async def test_update_risk(db_session: AsyncSession, sample_endpoints: list[Endpoint]):
    """Test updating endpoint risk classification."""
    repo = EndpointRepository(db_session)
    target_id = sample_endpoints[0].id

    updated = await repo.update_risk(target_id, "high", 0.75)

    assert updated is not None
    assert updated.risk_tier == "high"
    assert updated.risk_score == 0.75


@pytest.mark.asyncio
async def test_update_migration_status(db_session: AsyncSession, sample_endpoints: list[Endpoint]):
    """Test updating endpoint migration status."""
    repo = EndpointRepository(db_session)
    target_id = sample_endpoints[0].id

    updated = await repo.update_migration_status(
        target_id, "complete", "ML-KEM-768"
    )

    assert updated is not None
    assert updated.migration_status == "complete"
    assert updated.migrated_algorithm == "ML-KEM-768"
