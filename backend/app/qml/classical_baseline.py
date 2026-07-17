"""Classical SVM baseline classifier."""

import numpy as np
import joblib
from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score


class SVMClassifier:
    """SVM classifier with identical interface to VQCClassifier."""

    def __init__(self):
        self.model = SVC(kernel='rbf', C=1.0, probability=True, random_state=42)
        self.encoder = LabelEncoder()

    def fit(self, X: np.ndarray, y: np.ndarray) -> dict:
        """Train SVM classifier.

        Args:
            X: Shape (n_samples, 6) feature matrix
            y: Shape (n_samples,) class labels

        Returns:
            Dict with training accuracy
        """
        y_encoded = self.encoder.fit_transform(y)
        self.model.fit(X, y_encoded)

        y_pred_encoded = self.model.predict(X)
        accuracy = accuracy_score(y_encoded, y_pred_encoded)

        return {"accuracy": accuracy}

    def predict(self, X: np.ndarray) -> list[str]:
        """Predict class labels.

        Args:
            X: Shape (n_samples, 6) feature matrix

        Returns:
            List of predicted class labels
        """
        y_pred_encoded = self.model.predict(X)
        return list(self.encoder.inverse_transform(y_pred_encoded))

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities.

        Args:
            X: Shape (n_samples, 6) feature matrix

        Returns:
            Shape (n_samples, n_classes) probability matrix
        """
        return self.model.predict_proba(X)

    def save(self, path: str) -> None:
        """Save classifier to disk."""
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: str) -> "SVMClassifier":
        """Load classifier from disk."""
        return joblib.load(path)
