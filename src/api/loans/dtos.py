from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class CreateLoanDTO(BaseModel):
  """DTO para crear un nuevo préstamo"""
  copy_id: int = Field(..., description="ID del ejemplar a prestar")
  user_id: UUID = Field(..., description="UUID del usuario que toma el préstamo")

  model_config = ConfigDict(from_attributes=True)


class LoanDTO(CreateLoanDTO):
  """DTO de préstamo con todos los campos básicos"""
  id_loan: int = Field(..., description="ID único del préstamo")
  loan_date: date = Field(..., description="Fecha de creación del préstamo")
  due_date: date = Field(..., description="Fecha de vencimiento del préstamo")
  return_date: Optional[date] = Field(None, description="Fecha de devolución (null si no ha sido devuelto)")
  loan_status_id: int = Field(..., description="ID del estado del préstamo (1=activo, 2=devuelto, 3=vencido)")
  created_at: datetime = Field(..., description="Fecha de creación del registro en base de datos")
  updated_at: datetime = Field(..., description="Fecha de última actualización del registro")

  model_config = ConfigDict(from_attributes=True)


class LoanFilterDTO(BaseModel):
  """DTO de filtros para paginación de préstamos"""
  id_status: int = Field(default=0, description="ID del estado para filtrar (0 = todos, 1=activo, 2=devuelto, 3=vencido)")


class LoanDetailDTO(BaseModel):
  """DTO plano para listados con datos esenciales de préstamo, usuario y libro"""
  id_loan: int = Field(..., description="ID único del préstamo")
  loan_date: date = Field(..., description="Fecha de creación del préstamo")
  due_date: date = Field(..., description="Fecha de vencimiento del préstamo")
  return_date: Optional[date] = Field(None, description="Fecha de devolución (null si no ha sido devuelto)")
  loan_status_id: int = Field(..., description="ID del estado del préstamo (1=activo, 2=devuelto, 3=vencido)")
  loan_status_name: str = Field(..., description="Nombre del estado del préstamo")
  user_id: UUID = Field(..., description="UUID del usuario que tiene el préstamo")
  user_name: str = Field(..., description="Nombre completo del usuario")
  copy_id: int = Field(..., description="ID del ejemplar prestado")
  copy_barcode: str = Field(..., description="Código de barras del ejemplar")
  copy_signature: str = Field(..., description="Signatura topográfica del ejemplar")
  book_id: int = Field(..., description="ID del libro al que pertenece el ejemplar")
  book_title: str = Field(..., description="Título del libro")

  model_config = ConfigDict(from_attributes=True)