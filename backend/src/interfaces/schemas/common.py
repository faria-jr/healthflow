"""Common schemas."""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response."""

    model_config = ConfigDict(from_attributes=True)

    success: bool = True
    data: T | None = None
    error: str | None = None
    meta: dict[str, Any] | None = None


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    total: int
    limit: int
    offset: int
    has_more: bool


class PaginatedResponse(ApiResponse[T], Generic[T]):
    """Paginated API response."""

    meta: PaginationMeta


class ErrorResponse(BaseModel):
    """Error response."""

    detail: str
    code: str | None = None
    field: str | None = None
