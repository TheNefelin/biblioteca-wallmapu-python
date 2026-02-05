from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class PaginationResponseDTO(BaseModel, Generic[T]): 
  total_count: int
  total_pages: int
  current_page: int
  page_size: int
  next: Optional[str] = None
  prev: Optional[str] = None
  result: T

class PaginationRequestDTO(BaseModel, Generic[T]): 
  count: int
  result: T