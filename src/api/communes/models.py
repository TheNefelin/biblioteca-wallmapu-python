from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class Commune(Base):
  __tablename__ = "wm_communes"

  id_commune = Column(Integer, primary_key=True, autoincrement=True)
  commune = Column(String(45), nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
  province_id = Column(Integer, ForeignKey('wm_provinces.id_province'))

  province = relationship("Province", back_populates="communes")