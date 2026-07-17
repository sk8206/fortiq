"""Application configuration using pydantic-settings."""

import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Find .env file in backend/ directory
_backend_dir = Path(__file__).resolve().parent.parent.parent
_env_file = _backend_dir / ".env"

# Database paths: /tmp on Vercel, local file otherwise
if "VERCEL" in os.environ:
    _sqlite_path = "/tmp/fortiq.db"
else:
    _sqlite_path = str(_backend_dir / "fortiq.db")


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database - two separate URLs for async and sync
    DATABASE_URL: str = f"sqlite+aiosqlite:///{_sqlite_path}"
    SYNC_DATABASE_URL: str = f"sqlite:///{_sqlite_path}"

    # Redis (Optional when not running Celery)
    REDIS_URL: str = ""

    # Auth
    SECRET_KEY: str = "fortiq-default-secret-key-change-in-prod-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

    # Environment
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Model paths
    VQC_PARAMS_PATH: str = "models/vqc_params.npy"
    SVM_MODEL_PATH: str = "models/svm_model.pkl"
    NORMALIZER_PATH: str = "models/normalizer.pkl"

    model_config = SettingsConfigDict(
        env_file=str(_env_file),
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()

