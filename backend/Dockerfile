# Fortiq Backend Dockerfile
# Python 3.11 with liboqs build dependencies for PQC operations

FROM python:3.11-slim-bookworm

# Install system dependencies for liboqs (C library for PQC)
RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    ninja-build \
    libssl-dev \
    pkg-config \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini .
COPY scripts/ ./scripts/

# Create models directory for trained models
RUN mkdir -p models

# Create non-root user for security
RUN useradd -m -u 1000 fortiq && chown -R fortiq:fortiq /app
USER fortiq

# Expose FastAPI port
EXPOSE 8000

# Default command: run FastAPI with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
