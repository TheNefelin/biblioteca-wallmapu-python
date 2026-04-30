from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.database import Base


class Notification(Base):
  __tablename__ = "wm_notifications"

  id_notification = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String(100), nullable=False)
  message = Column(Text, nullable=False)
  is_priority = Column(Boolean, default=False)
  is_read = Column(Boolean, default=False)
  created_at = Column(DateTime, server_default=func.now())

  user_id = Column(UUID(as_uuid=True), ForeignKey("wm_users.id_user"), nullable=False)
  user = relationship("User")
