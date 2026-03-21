from datetime import date
from pydantic import BaseModel, ConfigDict
from typing import Optional


class LoanDTO(BaseModel):
  id_loan: int
  loan_date: date
  due_date: date
  return_date: Optional[date] = None
  status: str
  copy_id: int
  user_id: str

  model_config = ConfigDict(from_attributes=True)


class LoanDetailDTO(BaseModel):
  id_loan: int
  loan_date: date
  due_date: date
  return_date: Optional[date] = None
  status: str
  copy_id: int
  user_id: str
  user_name: Optional[str] = None
  user_lastname: Optional[str] = None
  book_id: Optional[int] = None
  book_title: Optional[str] = None
  copy_barcode: Optional[str] = None

  model_config = ConfigDict(from_attributes=True)


class CreateLoanDTO(BaseModel):
  copy_id: int
  user_id: str
  due_date: Optional[date] = None


class ReturnLoanDTO(BaseModel):
  return_date: date
