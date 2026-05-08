import uuid
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String,DateTime, func, text, UUID

from src.core.database import Base

class User(Base):
  __tablename__ = "wm_users"

  id_user = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  email = Column(String(100), nullable=False, unique=True)
  name = Column(String(100))
  lastname = Column(String(100))
  rut = Column(String(12), unique=True)
  address = Column(String(256))
  phone = Column(String(10))
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())  

  commune_id = Column(Integer, ForeignKey("wm_communes.id_commune"))
  user_role_id = Column(Integer, ForeignKey("wm_user_role.id_user_role"), default=3)
  user_status_id = Column(Integer, ForeignKey("wm_user_status.id_user_status"), default=1)

  commune = relationship("Commune", back_populates="users")
  user_role = relationship("UserRole", back_populates="users")
  user_status = relationship("UserStatus", back_populates="users")
  reservations = relationship("Reservation", back_populates="user")
