"""Authentication API routes."""

from uuid import UUID

from fastapi import APIRouter, HTTPException, Response, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy import select
from starlette.requests import Request

from app.core.dependencies import CurrentUser, DbSession
from app.core.security import create_access_token, decode_token
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, UserResponse
from app.schemas.common import ResponseEnvelope, ok
from app.services.auth_service import AuthService

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/login", response_model=ResponseEnvelope[AuthResponse])
@limiter.limit("5/minute")
async def login(
    request: Request,
    response: Response,
    login_data: LoginRequest,
    db: DbSession,
):
    """Authenticate user and return access token."""
    service = AuthService(db)
    result = await service.authenticate(login_data.username, login_data.password)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    auth_response, refresh_token = result

    # Set refresh token as HttpOnly cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="strict",
        secure=False,  # Set to True in production with HTTPS
        max_age=7 * 24 * 60 * 60,  # 7 days
    )

    return ok(auth_response)


@router.post("/logout")
async def logout(response: Response):
    """Clear refresh token cookie."""
    response.delete_cookie(key="refresh_token")
    return ok({"message": "Logged out successfully"})


@router.post("/refresh", response_model=ResponseEnvelope[AuthResponse])
async def refresh_token(
    request: Request,
    db: DbSession,
):
    """Refresh access token using refresh cookie."""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing",
        )

    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    # Get user
    result = await db.execute(select(User).where(User.id == UUID(user_id)))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    # Create new access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return ok(
        AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )
    )


@router.get("/me", response_model=ResponseEnvelope[UserResponse])
async def get_current_user(user: CurrentUser):
    """Get current authenticated user."""
    return ok(UserResponse.model_validate(user))
