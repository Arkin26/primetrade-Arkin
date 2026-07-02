from typing import Generic, List, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: list[dict] | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    limit: int
    pages: int
