"""Common Pydantic schemas for API responses."""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    total: int
    page: int
    per_page: int
    total_pages: int


class ErrorDetail(BaseModel):
    """Error detail for API responses."""

    code: str
    message: str
    detail: Any = None


class ResponseEnvelope(BaseModel, Generic[T]):
    """Standard API response envelope."""

    data: T | None = None
    meta: PaginationMeta | None = None
    error: ErrorDetail | None = None


def ok(data: T, meta: PaginationMeta | None = None) -> ResponseEnvelope[T]:
    """Create a successful response."""
    return ResponseEnvelope(data=data, meta=meta)


def err(code: str, message: str, detail: Any = None) -> ResponseEnvelope[None]:
    """Create an error response."""
    return ResponseEnvelope(error=ErrorDetail(code=code, message=message, detail=detail))
