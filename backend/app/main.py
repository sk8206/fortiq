"""FastAPI application factory."""

from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.core.config import settings
from app.core.logging import LoggingMiddleware, configure_logging
from app.routers import admin, auth, classify, endpoints, migrate

# Configure structured logging
configure_logging()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger = structlog.get_logger()
    logger.info("fortiq_api_started", env=settings.ENVIRONMENT)

    # Automatically initialize SQLite database schemas & seed data
    try:
        from app.core.database import sync_engine
        from app.core.init_db import initialize_sqlite_db
        initialize_sqlite_db(sync_engine)
    except Exception as e:
        logger.error("database_initialization_failed", error=str(e))

    yield
    logger.info("fortiq_api_stopped")



def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Fortiq API",
        description="Post-Quantum Cryptography Migration Platform",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )
    app.add_middleware(LoggingMiddleware)

    # Rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Include routers
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(endpoints.router, prefix="/api/v1/endpoints", tags=["endpoints"])
    app.include_router(classify.router, prefix="/api/v1/classify", tags=["classify"])
    app.include_router(migrate.router, prefix="/api/v1/migrate", tags=["migrate"])
    app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

    @app.get("/health")
    async def health():
        """Health check endpoint for Docker."""
        return {"status": "ok"}

    return app


app = create_app()
