"""Authentication Pydantic schemas."""

from uuid import UUID

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Login request schema."""

    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    """User response schema."""

    id: UUID
    username: str
    is_active: bool

    model_config = {"from_attributes": True}


class AuthResponse(BaseModel):
    """Full auth response with token and user."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse
