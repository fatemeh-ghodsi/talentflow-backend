

from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginationMetadata(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    page_size: int


class PaginatedResponse(GenericModel, Generic[T]):
    items: list[T]
    metadata: PaginationMetadata