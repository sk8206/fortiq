"""Pytest configuration and fixtures."""

import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio

# Override settings database URLs before importing app modules
from app.core.config import settings
settings.DATABASE_URL = settings.DATABASE_URL.replace("fortiq.db", "fortiq_test.db").replace("fortiq", "fortiq_test")
settings.SYNC_DATABASE_URL = settings.SYNC_DATABASE_URL.replace("fortiq.db", "fortiq_test.db").replace("fortiq", "fortiq_test")

from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.database import get_db, async_engine
from app.main import app
from app.models import Base


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Create test database engine."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_engine
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a database session for tests."""
    from sqlalchemy import text
    
    # Ensure a clean database before each test
    async with test_engine.begin() as conn:
        await conn.execute(text("PRAGMA foreign_keys = OFF;"))
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())
        await conn.execute(text("PRAGMA foreign_keys = ON;"))

    session_factory = async_sessionmaker(
        test_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with session_factory() as session:
        yield session
        await session.rollback()



@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP client for testing."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_client(client: AsyncClient, db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create an authenticated HTTP client."""
    from app.models.user import User
    from app.core.security import get_password_hash, create_access_token

    # Create test user
    user = User(
        username="testuser",
        hashed_password=get_password_hash("testpassword"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Create access token
    token = create_access_token(data={"sub": str(user.id)})

    # Set auth header
    client.headers["Authorization"] = f"Bearer {token}"

    yield client
