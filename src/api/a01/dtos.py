from datetime import date, datetime
from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field
from sqlalchemy import true

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
  isSuccess: bool
  statusCode: int
  message: str
  data: Optional[T] 

class BoricResponse(BaseModel):
  text: str
  timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
