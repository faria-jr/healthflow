"""Pagination DTOs."""

from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Pagination parameters."""
    
    cursor: Optional[str] = None
    limit: int = 20
    
    class Config:
        frozen = True


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response."""
    
    items: list[T]
    next_cursor: Optional[str] = None
    has_more: bool = False
    total: Optional[int] = None
    
    class Config:
        frozen = True


def encode_cursor(id: int) -> str:
    """Encode ID to cursor string."""
    import base64
    return base64.b64encode(str(id).encode()).decode()


def decode_cursor(cursor: str) -> int:
    """Decode cursor string to ID."""
    import base64
    return int(base64.b64decode(cursor.encode()).decode())
