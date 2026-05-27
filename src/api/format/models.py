from sqlalchemy import Column, DateTime, Integer, String, func

from src.core.database import Base


class Format(Base):
  __tablename__ = "wm_formats"

  id_format = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(200), nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
