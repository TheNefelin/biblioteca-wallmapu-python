from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class Edition(Base):
  __tablename__ = "wm_editions"

  id_edition = Column(Integer, primary_key=True, autoincrement=True)
  edition = Column(String(20), nullable=True)
  isbn = Column(String(20), nullable=False)
  publication_year = Column(Integer, nullable=False)
  pages = Column(Integer, nullable=False)
  cover_image = Column(String(256), nullable=True)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
  editorial_id = Column(Integer, ForeignKey('wm_editorials.id_editorial'))

  book_id = Column(Integer, ForeignKey('wm_books.id_book'))
  book = relationship("Book", back_populates="editions")
