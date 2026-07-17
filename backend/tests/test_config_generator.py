"""Tests for migration config generator."""

import pytest

from app.models.endpoint import Endpoint
from app.pqc.config_generator import generate_migration_configs


def test_generate_configs_api():
    """Test config generation for API endpoint."""
    endpoint = Endpoint(
        name="test-api",
        host="10.0.0.1",
        port=443,
        endpoint_type="api",
        algorithm="RSA-2048",
        key_length=2048,
        data_sensitivity=3,
        exposure_surface="internet-facing",
        traffic_volume="high",
        cert_expiry_days=365,
        risk_tier="high",
        migration_status="pending",
    )

    configs = generate_migration_configs(endpoint)

    assert isinstance(configs, list)
    assert len(configs) > 0
    assert any("ML-KEM-768" in cfg for cfg in configs)
    assert any("nginx" in cfg.lower() or "tls" in cfg.lower() for cfg in configs)


def test_generate_configs_database():
    """Test config generation for database endpoint."""
    endpoint = Endpoint(
        name="test-db",
        host="10.0.0.2",
        port=5432,
        endpoint_type="database",
        algorithm="ECC-256",
        key_length=256,
        data_sensitivity=5,
        exposure_surface="internal",
        traffic_volume="medium",
        cert_expiry_days=100,
        risk_tier="critical",
        migration_status="pending",
    )

    configs = generate_migration_configs(endpoint)

    assert isinstance(configs, list)
    assert len(configs) > 0
    assert any("ML-DSA-65" in cfg for cfg in configs)


def test_generate_configs_all_types():
    """Test all endpoint types produce configs."""
    types = ["api", "database", "iot", "firmware", "web"]

    for ep_type in types:
        endpoint = Endpoint(
            name=f"test-{ep_type}",
            host="10.0.0.1",
            port=443,
            endpoint_type=ep_type,
            algorithm="RSA-2048",
            key_length=2048,
            data_sensitivity=3,
            exposure_surface="internal",
            traffic_volume="medium",
            cert_expiry_days=365,
            risk_tier="medium",
            migration_status="pending",
        )

        configs = generate_migration_configs(endpoint)
        assert len(configs) > 0, f"No configs generated for {ep_type}"
