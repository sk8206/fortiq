"""User repository for authentication."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    """Repository for User entity database operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_username(self, username: str) -> User | None:
        """Get a user by username."""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def create(self, username: str, hashed_password: str) -> User:
        """Create a new user."""
        user = User(username=username, hashed_password=hashed_password)
        self.db.add(user)
        await self.db.flush()
        return user
