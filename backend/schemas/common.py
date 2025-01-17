from typing import Generic, List, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    total_pages: int = Field(..., description="Total number of pages.")
    total_items: int = Field(..., description="Total number of items.")
    current_page: int = Field(..., description="Current page number.")
    items: List[T] = Field(..., description="List of items on the current page.")
