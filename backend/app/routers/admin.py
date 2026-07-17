"""Admin API routes for data generation and model training."""

import random
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.core.dependencies import CurrentUser, DbSession
from app.models.endpoint import Endpoint
from app.schemas.common import ResponseEnvelope, ok


router = APIRouter()


class GenerateDataRequest(BaseModel):
    count: int = 100


class GenerateDataResponse(BaseModel):
    created: int
    message: str


class TrainModelsResponse(BaseModel):
    message: str
    vqc_trained: bool
    svm_trained: bool


# Sample data for endpoint generation
ENDPOINT_TYPES = ["api", "database", "iot", "firmware", "web"]
ALGORITHMS = ["RSA-2048", "RSA-4096", "ECC-256", "ECC-384"]
KEY_LENGTHS = {"RSA-2048": 2048, "RSA-4096": 4096, "ECC-256": 256, "ECC-384": 384}
EXPOSURE_SURFACES = ["internet-facing", "internal", "air-gapped"]
TRAFFIC_VOLUMES = ["low", "medium", "high", "critical"]
SERVICES = [
    "auth", "payment", "user", "order", "inventory", "notification",
    "analytics", "reporting", "gateway", "storage", "cache", "queue",
    "search", "recommendation", "billing", "shipping", "support"
]
DOMAINS = ["api", "db", "svc", "app", "core", "edge", "internal"]


def generate_endpoint_name() -> str:
    service = random.choice(SERVICES)
    domain = random.choice(DOMAINS)
    suffix = random.randint(1, 99)
    return f"{service}-{domain}-{suffix:02d}"


def generate_endpoint() -> dict:
    algorithm = random.choice(ALGORITHMS)
    endpoint_type = random.choice(ENDPOINT_TYPES)
    exposure = random.choice(EXPOSURE_SURFACES)

    # Higher data sensitivity for certain types
    if endpoint_type in ["database", "api"]:
        data_sensitivity = random.uniform(0.5, 1.0)
    else:
        data_sensitivity = random.uniform(0.1, 0.8)

    # Cert expiry - some near expiry, some far
    cert_expiry = random.choice([
        random.randint(1, 30),      # Near expiry
        random.randint(30, 90),     # Medium
        random.randint(90, 365),    # Far
    ])

    return {
        "id": uuid4(),
        "name": generate_endpoint_name(),
        "host": f"{random.choice(SERVICES)}.internal.fortiq.io",
        "port": random.choice([443, 8443, 5432, 6379, 27017, 9200]),
        "endpoint_type": endpoint_type,
        "algorithm": algorithm,
        "key_length": KEY_LENGTHS[algorithm],
        "data_sensitivity": round(data_sensitivity, 2),
        "exposure_surface": exposure,
        "traffic_volume": random.choice(TRAFFIC_VOLUMES),
        "cert_expiry_days": cert_expiry,
        "migration_status": "pending",
    }


@router.post("/generate-data", response_model=ResponseEnvelope[GenerateDataResponse])
async def generate_data(
    request: GenerateDataRequest,
    db: DbSession,
    user: CurrentUser,
):
    """Generate sample endpoint data for testing."""
    if request.count < 1 or request.count > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Count must be between 1 and 1000"
        )

    created = 0
    for _ in range(request.count):
        endpoint_data = generate_endpoint()
        endpoint = Endpoint(**endpoint_data)
        db.add(endpoint)
        created += 1

    await db.commit()

    return ok(GenerateDataResponse(
        created=created,
        message=f"Successfully generated {created} sample endpoints"
    ))


@router.post("/train-models", response_model=ResponseEnvelope[TrainModelsResponse])
async def train_models(
    user: CurrentUser,
):
    """Train the VQC and SVM classification models."""
    # Get the path to the training script
    backend_dir = Path(__file__).resolve().parent.parent.parent
    script_path = backend_dir / "scripts" / "train_models.py"

    if not script_path.exists():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Training script not found"
        )

    try:
        # Run the training script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
            cwd=str(backend_dir)
        )

        if result.returncode != 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Training failed: {result.stderr}"
            )

        return ok(TrainModelsResponse(
            message="Models trained successfully",
            vqc_trained=True,
            svm_trained=True
        ))

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Training timed out after 10 minutes"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Training failed: {str(e)}"
        )
