from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship
from src.core.database import Base


class Editorial(Base):
  __tablename__ = "wm_editorials"

  id_editorial = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(200), nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

  editions = relationship("Edition", back_populates="editorial")
