from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from src.core.database import Base

class UserStatus(Base):
  __tablename__ = "wm_user_status"

  id_user_status = Column(Integer, primary_key=True, autoincrement=True)
  status = Column(String(45), nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

  users = relationship("User", back_populates="user_status")
