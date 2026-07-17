"""Tests for feature engineering."""

import numpy as np
import pytest

from app.models.endpoint import Endpoint
from app.qml.features import endpoint_to_features


def test_endpoint_to_features_basic():
    """Test feature extraction from endpoint."""
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
        risk_tier="unknown",
        migration_status="pending",
    )

    features = endpoint_to_features(endpoint)

    assert features.shape == (6,)
    assert 0.0 <= features[0] <= 1.0  # algorithm_risk
    assert features[1] == 0.6  # data_sensitivity: 3/5
    assert features[2] == 1.0  # exposure: internet-facing
    assert features[3] == 0.7  # traffic: high
    assert 0.0 <= features[4] <= 1.0  # cert_urgency
    assert 0.0 <= features[5] <= 1.0  # composite_risk


def test_algorithm_risk_mapping():
    """Test algorithm risk values."""
    from app.qml.features import ALGORITHM_RISK

    assert ALGORITHM_RISK["RSA-2048"] == 0.60
    assert ALGORITHM_RISK["RSA-4096"] == 0.30
    assert ALGORITHM_RISK["ECC-256"] == 0.50
    assert ALGORITHM_RISK["ECC-384"] == 0.20


import tempfile
from pathlib import Path

from app.qml.features import FeatureNormalizer


def test_feature_normalizer_fit_transform():
    """Test normalizer fit and transform."""
    X = np.array([
        [0.6, 0.6, 1.0, 0.7, 0.5, 0.68],
        [0.3, 0.4, 0.4, 0.4, 0.2, 0.34],
        [0.5, 0.8, 1.0, 1.0, 0.9, 0.84],
    ])

    normalizer = FeatureNormalizer()
    X_norm = normalizer.fit_transform(X)

    assert X_norm.shape == (3, 6)
    # After standardization, mean ~ 0, std ~ 1
    assert np.abs(X_norm.mean(axis=0)).max() < 0.1
    assert np.abs(X_norm.std(axis=0) - 1.0).max() < 0.1


def test_feature_normalizer_save_load():
    """Test normalizer persistence."""
    X = np.array([[0.6, 0.6, 1.0, 0.7, 0.5, 0.68]])

    normalizer = FeatureNormalizer()
    normalizer.fit_transform(X)

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "normalizer.pkl"
        normalizer.save(str(path))

        loaded = FeatureNormalizer.load(str(path))
        X_test = np.array([[0.3, 0.4, 0.4, 0.4, 0.2, 0.34]])
        result = loaded.transform(X_test)

        assert result.shape == (1, 6)


from app.qml.features import prepare_for_amplitude_encoding


def test_prepare_for_amplitude_encoding():
    """Test padding to 16 elements for 4-qubit circuit."""
    features = np.array([0.6, 0.6, 1.0, 0.7, 0.5, 0.68])

    padded = prepare_for_amplitude_encoding(features)

    assert padded.shape == (16,)
    assert np.array_equal(padded[:6], features)
    assert np.all(padded[6:] == 0.0)
