"""Authentication service for business logic."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.repositories.user_repository import UserRepository
from app.schemas.auth import AuthResponse, UserResponse


class AuthService:
    """Service for authentication business logic."""

    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def authenticate(self, username: str, password: str) -> AuthResponse | None:
        """Authenticate user and return tokens."""
        user = await self.repo.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        ), refresh_token

    async def create_user(self, username: str, password: str) -> UserResponse:
        """Create a new user."""
        hashed_password = get_password_hash(password)
        user = await self.repo.create(username, hashed_password)
        return UserResponse.model_validate(user)
