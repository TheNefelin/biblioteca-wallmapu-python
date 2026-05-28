from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class CreateNotificationDTO(BaseModel):
  title: str = Field(..., description="Título de la notificación (ej: 'PRÉSTAMO VENCIDO', 'ANUNCIO')")
  message: str = Field(..., description="Mensaje detallado de la notificación")
  is_priority: bool = Field(default=False, description="True = Alta prioridad (urgente), False = Normal")
  user_id: UUID = Field(..., description="UUID del usuario destinatario")


class UpdateNotificationDTO(BaseModel):
  id_notification: int = Field(..., description="ID único de la notificación")
  is_read: bool = Field(..., description="Estado de lectura: True = Leída, False = No leída")


class NotificationDTO(CreateNotificationDTO, UpdateNotificationDTO):
  created_at: datetime = Field(..., description="Fecha de creación de la notificación")

  model_config = ConfigDict(from_attributes=True)


class NotificationDetailDTO(NotificationDTO):
  email: str = Field(..., description="Email del usuario destinatario")


class NotificationFilterDTO(BaseModel):
  is_read: bool = Field(default=True, description="filtrar (true = todos, false = solo no leidas)")


class CreateNotificationByEmailDTO(BaseModel):
  email: str = Field(..., description="Email del usuario destinatario")
  title: str = Field(..., description="Título de la notificación")
  message: str = Field(..., description="Mensaje detallado de la notificación")
  is_priority: bool = Field(default=False, description="True = Alta prioridad, False = Normal")
