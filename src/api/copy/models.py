from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, text
from sqlalchemy.orm import relationship

from src.core.database import Base


class Copy(Base):
  __tablename__ = "wm_copies"

  id_copy = Column(Integer, primary_key=True, autoincrement=True)
  barcode = Column(String(100), unique=True, nullable=False)
  signature_topography = Column(String(100), nullable=False)
  copy_number = Column(Integer, nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

  status_id = Column(Integer, ForeignKey('wm_copy_status.id_status'))
  status = relationship("CopyStatus", back_populates="copies")

  edition_id = Column(Integer, ForeignKey('wm_editions.id_edition'))
  edition = relationship("Edition", back_populates="copies")

  loans = relationship("Loan", back_populates="copy")
  reservations = relationship("Reservation", back_populates="copy")
