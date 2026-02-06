from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class PaginationResponseDTO(BaseModel, Generic[T]): 
  count: int
  pages: int
  next: Optional[str] = None
  prev: Optional[str] = None
  result: T 
