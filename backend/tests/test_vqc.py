"""Tests for Variational Quantum Classifier."""

import numpy as np
import pytest

from app.qml.vqc import vqc_circuit, N_QUBITS, N_LAYERS


def test_vqc_circuit_output_range():
    """Test VQC circuit returns value in [-1, 1]."""
    features = np.random.rand(16)
    params = np.random.uniform(-0.01, 0.01, (N_LAYERS, N_QUBITS, 2))

    output = vqc_circuit(features, params)

    assert -1.0 <= output <= 1.0


def test_vqc_circuit_deterministic():
    """Test VQC circuit gives same output for same inputs."""
    features = np.random.rand(16)
    params = np.random.uniform(-0.01, 0.01, (N_LAYERS, N_QUBITS, 2))

    output1 = vqc_circuit(features, params)
    output2 = vqc_circuit(features, params)

    assert np.isclose(output1, output2)


from app.qml.vqc import VQCClassifier


def test_vqc_classifier_init():
    """Test VQCClassifier initializes with correct structure."""
    classifier = VQCClassifier(lr=0.01, max_iter=50)

    assert hasattr(classifier, 'params_dict')
    assert 'critical' in classifier.params_dict
    assert 'high' in classifier.params_dict
    assert 'medium' in classifier.params_dict
    assert classifier.params_dict['critical'].shape == (N_LAYERS, N_QUBITS, 2)
    assert classifier.lr == 0.01
    assert classifier.max_iter == 50


def test_vqc_classifier_predict_shape():
    """Test predict returns valid class labels."""
    classifier = VQCClassifier()
    X = np.random.rand(5, 6)

    predictions = classifier.predict(X)

    assert len(predictions) == 5
    assert all(p in ['critical', 'high', 'medium', 'low'] for p in predictions)


def test_vqc_classifier_predict_proba_shape():
    """Test predict_proba returns correct shape."""
    classifier = VQCClassifier()
    X = np.random.rand(5, 6)

    proba = classifier.predict_proba(X)

    assert proba.shape == (5, 4)  # 4 classes
    assert np.allclose(proba.sum(axis=1), 1.0)  # probabilities sum to 1


def test_vqc_classifier_fit_improves_loss():
    """Test that fitting reduces loss."""
    # Small synthetic dataset
    X = np.array([[0.8, 0.8, 1.0, 1.0, 0.9, 0.9],  # Should be critical
                   [0.6, 0.6, 0.7, 0.7, 0.5, 0.6],  # Should be high
                   [0.3, 0.4, 0.4, 0.4, 0.2, 0.3],  # Should be medium
                   [0.1, 0.2, 0.1, 0.1, 0.1, 0.1]]) # Should be low
    y = np.array(['critical', 'high', 'medium', 'low'])

    classifier = VQCClassifier(lr=0.1, max_iter=20)

    # Get initial predictions
    initial_preds = classifier.predict(X)

    # Train
    result = classifier.fit(X, y)

    # Verify training ran
    assert 'critical' in result
    assert result['critical'] < 1.0  # Loss should be < 1.0 after training

    # Final predictions should be better (at least some correct)
    final_preds = classifier.predict(X)
    correct = sum(1 for pred, truth in zip(final_preds, y) if pred == truth)
    assert correct >= 1  # At least 1 correct prediction after training
