from sqlalchemy import Column, DateTime, Integer, String, func

from src.core.database import Base

class Region(Base):
  __tablename__ = "wm_regions"

  id_region = Column(Integer, primary_key=True, autoincrement=True)
  region = Column(String(100), nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

