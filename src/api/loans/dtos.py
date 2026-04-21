from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional


class CreateLoanDTO(BaseModel):
  copy_id: int
  user_id: UUID

  model_config = ConfigDict(from_attributes=True)


class LoanDTO(CreateLoanDTO):
  id_loan: int
  loan_date: date
  due_date: date
  return_date: Optional[date] = None
  loan_status_id: int
  created_at: datetime
  updated_at: datetime


class ReturnLoanDTO(BaseModel):
  return_date: date


class LoanFilterDTO(BaseModel):
  id_status: int = Field(default=0, description="ID del Loan Status para filtrar (0 = todos)")

