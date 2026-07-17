"""Tests for SVM baseline classifier."""

import numpy as np
import pytest
import tempfile
from pathlib import Path

from app.qml.classical_baseline import SVMClassifier


def test_svm_classifier_init():
    """Test SVM classifier initialization."""
    classifier = SVMClassifier()

    assert hasattr(classifier, 'model')
    assert hasattr(classifier, 'encoder')


def test_svm_classifier_fit():
    """Test SVM fitting."""
    X = np.array([[0.6, 0.6, 1.0, 0.7, 0.5, 0.68],
                   [0.3, 0.4, 0.4, 0.4, 0.2, 0.34],
                   [0.5, 0.8, 1.0, 1.0, 0.9, 0.84],
                   [0.2, 0.2, 0.1, 0.1, 0.1, 0.14]])
    y = np.array(['high', 'medium', 'critical', 'low'])

    classifier = SVMClassifier()
    metrics = classifier.fit(X, y)

    assert 'accuracy' in metrics


def test_svm_classifier_predict():
    """Test SVM prediction."""
    X_train = np.array([[0.6, 0.6, 1.0, 0.7, 0.5, 0.68],
                        [0.3, 0.4, 0.4, 0.4, 0.2, 0.34],
                        [0.5, 0.8, 1.0, 1.0, 0.9, 0.84],
                        [0.2, 0.2, 0.1, 0.1, 0.1, 0.14]])
    y_train = np.array(['high', 'medium', 'critical', 'low'])

    classifier = SVMClassifier()
    classifier.fit(X_train, y_train)

    X_test = np.array([[0.6, 0.6, 1.0, 0.7, 0.5, 0.68]])
    predictions = classifier.predict(X_test)

    assert len(predictions) == 1
    assert predictions[0] in ['critical', 'high', 'medium', 'low']


def test_svm_classifier_save_load():
    """Test SVM persistence."""
    X = np.array([[0.6, 0.6, 1.0, 0.7, 0.5, 0.68],
                   [0.3, 0.4, 0.4, 0.4, 0.2, 0.34]])
    y = np.array(['high', 'medium'])

    classifier = SVMClassifier()
    classifier.fit(X, y)

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "svm.pkl"
        classifier.save(str(path))

        loaded = SVMClassifier.load(str(path))
        predictions = loaded.predict(X)

        assert len(predictions) == 2
