from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from src.core.database import Base

class UserRole(Base):
  __tablename__ = "wm_user_role"

  id_user_role = Column(Integer, primary_key=True, autoincrement=True)
  role = Column(String(45), nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

  users = relationship("User", back_populates="user_role")
