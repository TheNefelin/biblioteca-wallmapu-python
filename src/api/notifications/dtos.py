from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class NotificationDTO(BaseModel):
  id_notification: int
  title: str
  message: str
  is_read: bool
  user_id: str
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)


class NotificationDetailDTO(BaseModel):
  id_notification: int
  title: str
  message: str
  is_read: bool
  user_id: str
  user_name: Optional[str] = None
  user_email: Optional[str] = None
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)


class CreateNotificationDTO(BaseModel):
  title: str
  message: str
  user_id: str


class UpdateNotificationDTO(BaseModel):
  is_read: Optional[bool] = None
