import uuid
from src.core.database import Base
from sqlalchemy import Column, Integer, String,DateTime, func, text, UUID

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
  commune_id = Column(Integer)
  user_role_id = Column(Integer, server_default=text('3'))
  user_status_id = Column(Integer, server_default=text('1'))
