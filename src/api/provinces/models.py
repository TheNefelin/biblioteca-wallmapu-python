from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from src.core.database import Base

class Province(Base):
  __tablename__ = "wm_provinces"

  id_province = Column(Integer, primary_key=True, autoincrement=True)
  province = Column(String(100), nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
  region_id = Column(Integer, ForeignKey('wm_regions.id_region'))

  region = relationship("Region", back_populates="provinces")
  communes = relationship("Commune", back_populates="province")