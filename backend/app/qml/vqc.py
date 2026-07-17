"""Variational Quantum Classifier implementation."""

import numpy as np
from typing import Any, Callable, Optional


N_QUBITS = 4
N_LAYERS = 3


def vqc_circuit(features: np.ndarray, params: np.ndarray) -> float:
    """Pure NumPy simulation of the 4-qubit, 3-layer quantum circuit."""
    # Normalize features for Amplitude Embedding
    norm = np.linalg.norm(features)
    if norm > 1e-9:
        features_norm = features / norm
    else:
        features_norm = np.zeros(16)
        features_norm[0] = 1.0

    psi = features_norm.astype(complex).copy().reshape((2, 2, 2, 2))

    # Helper to apply a single-qubit gate
    def apply_gate(state, U, wire):
        if wire == 0:
            return np.einsum('ij,jklm->iklm', U, state)
        elif wire == 1:
            return np.einsum('ij,kjlm->kilm', U, state)
        elif wire == 2:
            return np.einsum('ij,kljm->klim', U, state)
        elif wire == 3:
            return np.einsum('ij,klmj->klmi', U, state)
        return state

    # Helper to apply CNOT gate
    def apply_cnot(state, control, target):
        slices = [slice(None)] * 4
        slices[control] = 1
        target_slices = list(slices)
        target_slices[target] = [1, 0]
        state[tuple(slices)] = state[tuple(target_slices)]
        return state

    # Apply layers
    for layer in range(N_LAYERS):
        for qubit in range(N_QUBITS):
            theta = params[layer, qubit, 0]
            phi = params[layer, qubit, 1]
            
            # RY rotation gate
            ry = np.array([
                [np.cos(theta / 2), -np.sin(theta / 2)],
                [np.sin(theta / 2), np.cos(theta / 2)]
            ], dtype=complex)
            psi = apply_gate(psi, ry, qubit)
            
            # RZ rotation gate
            rz = np.array([
                [np.exp(-1j * phi / 2), 0],
                [0, np.exp(1j * phi / 2)]
            ], dtype=complex)
            psi = apply_gate(psi, rz, qubit)

        for qubit in range(N_QUBITS):
            psi = apply_cnot(psi, qubit, (qubit + 1) % N_QUBITS)

    # Compute expectation value of PauliZ on wire 0
    expval = np.sum(np.abs(psi[0, :, :, :])**2) - np.sum(np.abs(psi[1, :, :, :])**2)
    return float(expval)


import joblib
from app.qml.features import prepare_for_amplitude_encoding



class VQCClassifier:
    """One-vs-rest VQC for multi-class risk classification."""

    CLASSES = ['critical', 'high', 'medium']  # 'low' is residual

    def __init__(
        self,
        lr: float = 0.01,
        max_iter: int = 100,
        progress_callback: Optional[Callable[[str, int, float, float], None]] = None,
    ):
        self.lr = lr
        self.max_iter = max_iter
        self.progress_callback = progress_callback

        self.params_dict = {
            cls: np.random.uniform(-0.01, 0.01, (N_LAYERS, N_QUBITS, 2))
            for cls in self.CLASSES
        }

    def predict(self, X) -> list[str]:
        proba = self.predict_proba(X)
        class_indices = np.argmax(proba, axis=1)
        all_classes = self.CLASSES + ['low']
        return [all_classes[i] for i in class_indices]

    def predict_proba(self, X) -> np.ndarray:
        # Convert to numpy array if needed (allows list input)
        X = np.asarray(X)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        n_samples = X.shape[0]
        scores = np.zeros((n_samples, len(self.CLASSES)))
        for i, cls in enumerate(self.CLASSES):
            params = self.params_dict[cls]
            for j, sample in enumerate(X):
                features_padded = prepare_for_amplitude_encoding(sample)
                expectation = vqc_circuit(features_padded, params)
                scores[j, i] = (expectation + 1.0) / 2.0
        low_scores = 1.0 - scores.max(axis=1, keepdims=True)
        scores = np.hstack([scores, low_scores])
        scores = scores / scores.sum(axis=1, keepdims=True)
        return scores

    def fit(self, X: np.ndarray, y: np.ndarray, log_fn: Any = None) -> dict:
        losses = {}

        for cls in self.CLASSES:
            y_binary = (y == cls).astype(int)
            params = self.params_dict[cls]

            for iteration in range(self.max_iter):
                grad = np.zeros_like(params)
                loss = 0.0

                for i, sample in enumerate(X):
                    features_padded = prepare_for_amplitude_encoding(sample)

                    expectation = vqc_circuit(features_padded, params)
                    prediction = (expectation + 1.0) / 2.0
                    prediction = np.clip(prediction, 1e-7, 1 - 1e-7)

                    sample_loss = -(
                        y_binary[i] * np.log(prediction) +
                        (1 - y_binary[i]) * np.log(1 - prediction)
                    )
                    loss += sample_loss

                    shift = 0.01
                    for layer in range(N_LAYERS):
                        for qubit in range(N_QUBITS):
                            for angle in range(2):
                                params[layer, qubit, angle] += shift
                                exp_up = vqc_circuit(features_padded, params)
                                pred_up = (exp_up + 1.0) / 2.0

                                params[layer, qubit, angle] -= 2 * shift
                                exp_down = vqc_circuit(features_padded, params)
                                pred_down = (exp_down + 1.0) / 2.0

                                params[layer, qubit, angle] += shift

                                grad[layer, qubit, angle] += (pred_up - pred_down) / (2 * shift) * (
                                    (prediction - y_binary[i]) / (prediction * (1 - prediction) + 1e-7)
                                )

                loss /= len(X)
                grad /= len(X)
                grad_norm = float(np.linalg.norm(grad))

                params -= self.lr * grad

                # Fire progress callback every iteration
                if self.progress_callback:
                    self.progress_callback(cls, iteration + 1, float(loss), grad_norm)

                # Legacy log_fn support
                if log_fn and (iteration + 1) % 10 == 0:
                    log_fn(f"Class {cls}, Iteration {iteration + 1}/{self.max_iter}, Loss: {loss:.4f}")

            losses[cls] = float(loss)
            self.params_dict[cls] = params

        return losses

    def save(self, path: str) -> None:
        joblib.dump(self.params_dict, path)

    @classmethod
    def load(cls, path: str) -> "VQCClassifier":
        classifier = cls()
        classifier.params_dict = joblib.load(path)
        return classifier