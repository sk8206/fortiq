from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin


class ModelEvaluation(Base, UUIDMixin):
    """
    ModelEvaluation entity storing VQC and SVM performance metrics.

    Used for the Model Comparison panel in the UI.
    """

    __tablename__ = "model_evaluations"

    model_type: Mapped[str] = mapped_column(String(20), nullable=False)  # vqc|svm
    binary_class: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # critical|high|medium (one-vs-rest)
    accuracy: Mapped[float] = mapped_column(Float, nullable=False)
    precision_score: Mapped[float] = mapped_column(Float, nullable=False)
    recall: Mapped[float] = mapped_column(Float, nullable=False)
    f1_score: Mapped[float] = mapped_column(Float, nullable=False)
    training_samples: Mapped[int] = mapped_column(Integer, nullable=False)
    test_samples: Mapped[int] = mapped_column(Integer, nullable=False)
    trained_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


    def __repr__(self) -> str:
        return f"<ModelEvaluation {self.model_type} {self.binary_class}: {self.accuracy:.2%}>"
