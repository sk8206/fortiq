#!/usr/bin/env python3
"""Train VQC and SVM models on endpoint dataset."""

import sys
import time
from pathlib import Path
from typing import Optional

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import SyncSessionLocal
from app.models.endpoint import Endpoint
from app.models.model_evaluation import ModelEvaluation
from app.qml.features import FeatureNormalizer, endpoint_to_features
from app.qml.vqc import VQCClassifier
from app.qml.classical_baseline import SVMClassifier


# ---------------------------------------------------------------------------
# Progress tracker — aware of VQC's per-class loop structure
# ---------------------------------------------------------------------------

class VQCProgressTracker:
    """
    Callback signature expected by VQCClassifier.fit():
        callback(cls: str, iteration: int, loss: float, grad_norm: float)

    Total steps = len(CLASSES) * max_iter, so the bar covers the full run.
    """

    CLASSES = ['critical', 'high', 'medium']

    def __init__(self, max_iter: int, bar_width: int = 30):
        self.max_iter = max_iter
        self.bar_width = bar_width
        self.total_steps = len(self.CLASSES) * max_iter
        self._start: Optional[float] = None

        # History keyed by class
        self.history: dict[str, list[tuple[int, float, float]]] = {
            c: [] for c in self.CLASSES
        }
        self._steps_done = 0

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _bar(self, pct: float) -> str:
        filled = int(self.bar_width * pct / 100)
        return "[" + "█" * filled + "░" * (self.bar_width - filled) + "]"

    @staticmethod
    def _fmt(sec: float) -> str:
        if sec != sec or sec < 0:   # nan or negative
            return "--:--"
        m, s = divmod(int(sec), 60)
        return f"{m:02d}:{s:02d}"

    # ------------------------------------------------------------------
    # Callback
    # ------------------------------------------------------------------

    def callback(self, cls: str, iteration: int, loss: float, grad_norm: float) -> None:
        if self._start is None:
            self._start = time.perf_counter()

        self._steps_done += 1
        self.history[cls].append((iteration, loss, grad_norm))

        elapsed = time.perf_counter() - self._start
        pct = 100.0 * self._steps_done / self.total_steps
        rate = elapsed / self._steps_done                          # sec / step
        eta = rate * (self.total_steps - self._steps_done)

        bar = self._bar(pct)
        is_last = (self._steps_done == self.total_steps)

        print(
            f"\r  {bar}"
            f"  [{cls:>8}] iter {iteration:>{len(str(self.max_iter))}}/{self.max_iter}"
            f"  loss={loss:8.5f}"
            f"  ‖∇‖={grad_norm:7.4f}"
            f"  {self._fmt(elapsed)} elapsed  ETA {self._fmt(eta)}",
            end="\n" if is_last else "",
            flush=True,
        )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------

    def print_summary(self) -> None:
        elapsed = time.perf_counter() - self._start if self._start else 0
        print(f"\n  ── VQC Training Summary ────────────────────────────────")
        for cls in self.CLASSES:
            entries = self.history[cls]
            if not entries:
                print(f"  {cls:>8} : no data")
                continue
            losses = [e[1] for e in entries]
            grads  = [e[2] for e in entries]
            delta  = losses[0] - losses[-1]
            direction = "↓ improved" if delta > 0 else ("↑ worsened" if delta < 0 else "→ flat")
            print(
                f"  {cls:>8} :  init={losses[0]:.5f}"
                f"  final={losses[-1]:.5f}"
                f"  Δ={delta:+.5f} {direction}"
                f"  min={min(losses):.5f}"
                f"  final‖∇‖={grads[-1]:.4f}"
            )
        print(f"  Wall time : {self._fmt(elapsed)}")
        print(f"  ────────────────────────────────────────────────────────\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("FORTIQ MODEL TRAINING")
    print("=" * 60)

    print("\n[1/8] Loading endpoints from database...")
    session = SyncSessionLocal()
    try:
        endpoints = session.query(Endpoint).all()
        print(f"Loaded {len(endpoints)} endpoints")

        X = np.array([endpoint_to_features(ep) for ep in endpoints])
        y = np.array([ep.risk_tier for ep in endpoints])
        print(f"Feature matrix shape: {X.shape}")
        print(f"Label distribution: {dict(zip(*np.unique(y, return_counts=True)))}")

        print("\n[2/8] Normalizing features...")
        normalizer = FeatureNormalizer()
        X_norm = normalizer.fit_transform(X)
        print("Normalization complete")

        print("\n[3/8] Splitting dataset (80/20 stratified)...")
        X_train, X_test, y_train, y_test = train_test_split(
            X_norm, y, test_size=0.20, random_state=42, stratify=y
        )
        print(f"Train: {len(X_train)}, Test: {len(X_test)}")

        MAX_ITER = 1
        print(f"\n[4/8] Training VQC classifier...")
        print(f"      {len(VQCProgressTracker.CLASSES)} classes × {MAX_ITER} iters"
              f" × {len(X_train)} samples × 25 param-shifts = "
              f"{len(VQCProgressTracker.CLASSES) * MAX_ITER * len(X_train) * 25:,} circuit evals")

        tracker = VQCProgressTracker(max_iter=MAX_ITER)

        vqc = VQCClassifier(
            lr=0.01,
            max_iter=MAX_ITER,
            progress_callback=tracker.callback,
        )
        vqc.fit(X_train, y_train)
        tracker.print_summary()

        print("\n[5/8] Training SVM baseline...")
        svm = SVMClassifier()
        svm.fit(X_train, y_train)
        print("SVM training complete")

        print("\n[6/8] Evaluating models on test set...")

        y_pred_vqc = vqc.predict(X_test)
        vqc_accuracy = accuracy_score(y_test, y_pred_vqc)
        vqc_precision, vqc_recall, vqc_f1, _ = precision_recall_fscore_support(
            y_test, y_pred_vqc, average="weighted", zero_division=0
        )
        print(f"\nVQC Results:")
        print(f"  Accuracy:  {vqc_accuracy:.4f}")
        print(f"  Precision: {vqc_precision:.4f}")
        print(f"  Recall:    {vqc_recall:.4f}")
        print(f"  F1-Score:  {vqc_f1:.4f}")

        y_pred_svm = svm.predict(X_test)
        svm_accuracy = accuracy_score(y_test, y_pred_svm)
        svm_precision, svm_recall, svm_f1, _ = precision_recall_fscore_support(
            y_test, y_pred_svm, average="weighted", zero_division=0
        )
        print(f"\nSVM Results:")
        print(f"  Accuracy:  {svm_accuracy:.4f}")
        print(f"  Precision: {svm_precision:.4f}")
        print(f"  Recall:    {svm_recall:.4f}")
        print(f"  F1-Score:  {svm_f1:.4f}")

        print("\n[7/8] Saving models...")
        models_dir = Path(__file__).parent.parent / "models"
        models_dir.mkdir(exist_ok=True)
        vqc.save(str(models_dir / "vqc_params.npy"))
        svm.save(str(models_dir / "svm_model.pkl"))
        normalizer.save(str(models_dir / "normalizer.pkl"))
        print(f"Models saved to {models_dir}/")

        print("\n[8/8] Storing evaluation metrics in database...")
        session.query(ModelEvaluation).delete()
        session.add(ModelEvaluation(
            model_type="vqc", binary_class="all",
            accuracy=float(vqc_accuracy), precision_score=float(vqc_precision),
            recall=float(vqc_recall), f1_score=float(vqc_f1),
            training_samples=len(X_train), test_samples=len(X_test),
        ))
        session.add(ModelEvaluation(
            model_type="svm", binary_class="all",
            accuracy=float(svm_accuracy), precision_score=float(svm_precision),
            recall=float(svm_recall), f1_score=float(svm_f1),
            training_samples=len(X_train), test_samples=len(X_test),
        ))
        session.commit()
        print("Evaluation metrics stored")

        print("\n" + "=" * 60)
        print("TRAINING COMPLETE")
        print("=" * 60)

    except Exception as e:
        session.rollback()
        print(f"\nError during training: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()