from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from src.api.loan_status.dtos import LoanStatusDTO
from src.api.users.dtos import UserMinimalDTO


class BookMinimalDTO(BaseModel):
  id_book: int
  title: str

  model_config = ConfigDict(from_attributes=True)


class EditionMinimalDTO(BaseModel):
  id_edition: int
  edition: str
  isbn: str
  book: BookMinimalDTO

  model_config = ConfigDict(from_attributes=True)


class CopyMinimalDTO(BaseModel):
  id_copy: int
  signature_topography: str
  barcode: str
  edition: EditionMinimalDTO

  model_config = ConfigDict(from_attributes=True)


class LoanDetailDTO(BaseModel):
  id_loan: int
  loan_date: date
  due_date: date
  return_date: Optional[date] = None
  created_at: datetime
  updated_at: datetime
  copy: CopyMinimalDTO
  user: UserMinimalDTO
  loan_status: LoanStatusDTO

  model_config = ConfigDict(from_attributes=True)
