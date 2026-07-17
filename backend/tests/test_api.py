"""Tests for API endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_unauthenticated_access(client: AsyncClient):
    """Test that unauthenticated requests are rejected."""
    response = await client.get("/api/v1/endpoints")
    assert response.status_code in [401, 403]


@pytest.mark.asyncio
async def test_list_endpoints(auth_client: AsyncClient):
    """Test listing endpoints with authentication."""
    response = await auth_client.get("/api/v1/endpoints")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_dashboard_stats(auth_client: AsyncClient):
    """Test dashboard stats endpoint."""
    response = await auth_client.get("/api/v1/endpoints/stats/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "total" in data["data"]
    assert "by_tier" in data["data"]
    assert "by_status" in data["data"]
    assert "compliance_score" in data["data"]
