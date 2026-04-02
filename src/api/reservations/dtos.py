from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from typing import Optional


class ReservationDTO(BaseModel):
  id_reservation: int
  reservation_date: datetime
  expiration_date: datetime
  user_id: UUID
  copy_id: int
  reservation_status_id: int

  model_config = ConfigDict(from_attributes=True)


class ReservationDetailDTO(BaseModel):
  id_reservation: int
  reservation_date: datetime
  expiration_date: datetime
  user_id: UUID
  user_name: Optional[str] = None
  user_lastname: Optional[str] = None
  user_email: Optional[str] = None
  copy_id: int
  copy_barcode: Optional[str] = None
  copy_signature: Optional[str] = None
  book_id: Optional[int] = None
  book_title: Optional[str] = None
  reservation_status_id: int
  reservation_status_name: Optional[str] = None

  model_config = ConfigDict(from_attributes=True)


class CreateReservationDTO(BaseModel):
  copy_id: int = Field(..., description="ID del ejemplar a reservar")


class ReservationPickupDTO(BaseModel):
  copy_id: int = Field(..., description="ID del ejemplar a entregar")
