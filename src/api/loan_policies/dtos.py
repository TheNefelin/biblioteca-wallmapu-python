from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class LoanPolicyDTO(BaseModel):
  id_policy: int = Field(..., description="Identificador único de la política de préstamo")
  name: Optional[str] = Field(None, description="Nombre de la política (ej: General, Estudiantes)")
  max_books: Optional[int] = Field(None, description="Cantidad máxima de libros que se pueden prestar")
  max_days: Optional[int] = Field(None, description="Número máximo de días de préstamo")
  reservation_days: Optional[int] = Field(3, description="Días que se mantiene una reserva activa")

  model_config = ConfigDict(from_attributes=True)

