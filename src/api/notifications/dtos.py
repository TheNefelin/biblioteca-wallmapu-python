from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class CreateNotificationDTO(BaseModel):
  """DTO para crear una nueva notificación"""
  title: str = Field(..., description="Título de la notificación (ej: 'PRÉSTAMO VENCIDO', 'ANUNCIO')")
  message: str = Field(..., description="Mensaje detallado de la notificación")
  is_priority: bool = Field(default=False, description="True = Alta prioridad (urgente), False = Normal")
  user_id: UUID = Field(..., description="UUID del usuario destinatario")

  model_config = ConfigDict(from_attributes=True)


class UpdateNotificationDTO(BaseModel):
  """DTO para actualizar una notificación existente"""
  id_notification: int = Field(..., description="ID único de la notificación")
  is_read: bool = Field(..., description="Estado de lectura: True = Leída, False = No leída")
  
  model_config = ConfigDict(from_attributes=True)


class NotificationDTO(CreateNotificationDTO, UpdateNotificationDTO):
  """DTO de notificación con todos los campos básicos"""
  created_at: datetime = Field(..., description="Fecha de creación de la notificación")


class NotificationDetailDTO(NotificationDTO):
  """DTO plano para listados con datos del usuario"""
  email: str = Field(..., description="Email del usuario destinatario")


class NotificationFilterDTO(BaseModel):
  is_read: bool = Field(default=True, description="filtrar (true = todos, false = solo los no leido)")


class CreateNotificationByEmailDTO(BaseModel):
  """DTO para crear notificación usando email en lugar de user_id"""
  email: str = Field(..., description="Email del usuario destinatario")
  title: str = Field(..., description="Título de la notificación")
  message: str = Field(..., description="Mensaje detallado de la notificación")
  is_priority: bool = Field(default=False, description="True = Alta prioridad, False = Normal")

  model_config = ConfigDict(from_attributes=True)
