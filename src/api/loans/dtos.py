from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional


class CreateLoanDTO(BaseModel):
  """DTO para crear un nuevo préstamo"""
  copy_id: int = Field(..., description="ID del ejemplar a prestar")
  user_id: UUID = Field(..., description="UUID del usuario que toma el préstamo")

  model_config = ConfigDict(from_attributes=True)


class LoanDTO(CreateLoanDTO):
  """DTO de préstamo con todos los campos básicos"""
  id_loan: int
  loan_date: date = Field(..., description="Fecha de préstamo")
  due_date: date = Field(..., description="Fecha de vencimiento")
  return_date: Optional[date] = Field(None, description="Fecha de devolución (null si no ha sido devuelto)")
  loan_status_id: int = Field(..., description="ID del estado del préstamo")
  created_at: datetime = Field(..., description="Fecha de creación del registro")
  updated_at: datetime = Field(..., description="Fecha de última actualización")


class ReturnLoanDTO(BaseModel):
  """DTO para registrar la devolución de un préstamo"""
  return_date: date = Field(..., description="Fecha de devolución del ejemplar")


class LoanFilterDTO(BaseModel):
  """DTO de filtros para paginación de préstamos"""
  id_status: int = Field(default=0, description="ID del Loan Status para filtrar (0 = todos, 1=activo, 2=devuelto, 3=vencido)")

