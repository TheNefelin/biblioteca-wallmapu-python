from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class EditionFormat(Base):
  __tablename__ = "wm_edition_format"

  id_edition = Column(Integer, ForeignKey("wm_editions.id_edition"), primary_key=True)
  id_format = Column(Integer, ForeignKey("wm_formats.id_format"), primary_key=True)
  created_at = Column(DateTime, server_default=func.now())

  edition = relationship("Edition", back_populates="edition_formats")
  format_rel = relationship("Format")
