"""Feature engineering for endpoint risk classification."""

import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

from app.models.endpoint import Endpoint


# Risk mappings
ALGORITHM_RISK = {
    "RSA-2048": 0.60,
    "RSA-4096": 0.30,
    "ECC-256": 0.50,
    "ECC-384": 0.20,
}

EXPOSURE_RISK = {
    "internet-facing": 1.0,
    "internal": 0.40,
    "air-gapped": 0.10,
}

TRAFFIC_RISK = {
    "critical": 1.0,
    "high": 0.70,
    "medium": 0.40,
    "low": 0.10,
}


def endpoint_to_features(endpoint: Endpoint) -> np.ndarray:
    """Extract 6 normalized features from endpoint.

    Returns:
        np.ndarray: Shape (6,) with features in [0, 1]
    """
    # Feature 1: algorithm risk
    alg_risk = ALGORITHM_RISK.get(endpoint.algorithm, 0.5)

    # Feature 2: data sensitivity normalized
    data_sens = endpoint.data_sensitivity / 5.0

    # Feature 3: exposure risk
    exp_risk = EXPOSURE_RISK.get(endpoint.exposure_surface, 0.5)

    # Feature 4: traffic risk
    traf_risk = TRAFFIC_RISK.get(endpoint.traffic_volume, 0.5)

    # Feature 5: cert urgency
    cert_urgency = np.clip((730 - endpoint.cert_expiry_days) / 760.0, 0.0, 1.0)

    # Feature 6: composite risk (mean of 1-5)
    features_partial = np.array([alg_risk, data_sens, exp_risk, traf_risk, cert_urgency])
    composite_risk = np.mean(features_partial)

    return np.array([alg_risk, data_sens, exp_risk, traf_risk, cert_urgency, composite_risk])


def prepare_for_amplitude_encoding(features: np.ndarray) -> np.ndarray:
    """Pad 6 features to 16 elements for AmplitudeEmbedding.

    PennyLane's AmplitudeEmbedding requires input size = 2^n_qubits.
    For 4 qubits: 2^4 = 16 elements.

    Args:
        features: Shape (6,) normalized feature vector

    Returns:
        np.ndarray: Shape (16,) zero-padded array
    """
    padded = np.zeros(16)
    padded[:6] = features
    return padded


class FeatureNormalizer:
    """Wrapper around StandardScaler for feature normalization."""

    def __init__(self):
        self.scaler = StandardScaler()
        self._fitted = False

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit scaler and transform data."""
        self._fitted = True
        return self.scaler.fit_transform(X)

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform data using fitted scaler."""
        if not self._fitted:
            raise ValueError("Normalizer not fitted. Call fit_transform first.")
        return self.scaler.transform(X)

    def save(self, path: str) -> None:
        """Save normalizer to disk."""
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: str) -> "FeatureNormalizer":
        """Load normalizer from disk."""
        return joblib.load(path)
