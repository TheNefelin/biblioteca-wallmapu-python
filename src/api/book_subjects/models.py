from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from src.core.database import Base

  
class BookSubject(Base):
  __tablename__ = "wm_book_subject"

  id_book = Column(Integer, ForeignKey("wm_books.id_book"), primary_key=True)
  id_subject = Column(Integer, ForeignKey("wm_subjects.id_subject"), primary_key=True)
  created_at = Column(DateTime, server_default=func.now())

  book = relationship("Book", back_populates="book_subjects")
  subject = relationship("Subject", back_populates="book_subjects")