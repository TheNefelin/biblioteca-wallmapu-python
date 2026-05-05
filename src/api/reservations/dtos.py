from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID


class CreateReservationDTO(BaseModel):
  """DTO para crear una nueva reserva"""
  copy_id: int = Field(..., description="ID del ejemplar a reservar")

  model_config = ConfigDict(from_attributes=True)


class ReservationDTO(CreateReservationDTO):
  id_reservation: Optional[int] = None
  reservation_date: Optional[datetime] = None
  expiration_date: datetime
  user_id: UUID
  reservation_status_id: Optional[int] = None


class ReservationDetailDTO(BaseModel):
  """DTO plano para listados con datos esenciales de reserva, usuario y libro"""
  id_reservation: int = Field(..., description="ID único de la reserva")
  reservation_date: datetime = Field(..., description="Fecha de creación de la reserva")
  expiration_date: datetime = Field(..., description="Fecha límite para retirar la reserva")
  user_id: UUID = Field(..., description="UUID del usuario que reserva")
  user_name: str = Field(..., description="Nombre del usuario")
  user_lastname: str = Field(..., description="Apellido del usuario")
  user_email: str = Field(..., description="Email del usuario")
  copy_id: int = Field(..., description="ID del ejemplar reservado")
  copy_barcode: str = Field(..., description="Código de barras del ejemplar")
  copy_signature: str = Field(..., description="Signatura topográfica del ejemplar")
  book_id: int = Field(..., description="ID del libro")
  book_title: str = Field(..., description="Título del libro")
  reservation_status_id: int = Field(..., description="ID del estado de la reserva")
  reservation_status_name: str = Field(..., description="Nombre del estado de la reserva")

  model_config = ConfigDict(from_attributes=True)


class ReservationPickupDTO(BaseModel):
  """DTO para confirmar retiro de reserva"""
  copy_id: int = Field(..., description="ID del ejemplar a entregar")

  model_config = ConfigDict(from_attributes=True)


class ReservationFilterDTO(BaseModel):
  """DTO de filtros para paginación de reservas"""
  id_status: int = Field(default=0, description="ID del estado para filtrar (0 = todos, 1=pendiente, 2=retirada, 3=cancelada, 4=vencida)")
