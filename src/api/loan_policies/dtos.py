from pydantic import BaseModel, ConfigDict
from typing import Optional


class LoanPolicyDTO(BaseModel):
  id_policy: int
  name: Optional[str] = None
  max_books: Optional[int] = None
  max_days: Optional[int] = None
  fine_per_day: Optional[float] = None
  reservation_days: Optional[int] = 3

  model_config = ConfigDict(from_attributes=True)


class CreateLoanPolicyDTO(BaseModel):
  name: str
  max_books: int
  max_days: int
  fine_per_day: float
  reservation_days: int = 3


class UpdateLoanPolicyDTO(BaseModel):
  name: Optional[str] = None
  max_books: Optional[int] = None
  max_days: Optional[int] = None
  fine_per_day: Optional[float] = None
  reservation_days: Optional[int] = None
