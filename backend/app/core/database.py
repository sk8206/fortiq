"""Database configuration with dual session architecture.

CRITICAL: FastAPI uses AsyncSession (asyncpg). Celery uses Session (psycopg2).
Never mix them - Celery workers have no asyncio event loop.
"""

from contextlib import contextmanager
from typing import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

# ── ENGINE 1: Async ── for FastAPI routes
is_sqlite = settings.DATABASE_URL.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

async_engine = create_async_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=settings.ENVIRONMENT == "development",
    **({} if is_sqlite else {"pool_size": 10, "max_overflow": 20})
)
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

# ── ENGINE 2: Sync ── for Celery tasks ONLY
sync_engine = create_engine(
    settings.SYNC_DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=settings.ENVIRONMENT == "development",
    **({} if is_sqlite else {"pool_size": 5, "max_overflow": 10})
)
SyncSessionLocal = sessionmaker(sync_engine, expire_on_commit=False)



async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for async database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


@contextmanager
def get_sync_db() -> Generator[Session, None, None]:
    """Celery context manager for sync database sessions."""
    session = SyncSessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
