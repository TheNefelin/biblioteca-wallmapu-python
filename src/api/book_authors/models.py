from sqlalchemy import Column, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class BookAuthor(Base):
  __tablename__ = "wm_book_author"

  id_book = Column(Integer, ForeignKey("wm_books.id_book"), primary_key=True)
  id_author = Column(Integer, ForeignKey("wm_authors.id_author"), primary_key=True)
  created_at = Column(DateTime, server_default=func.now())

  book = relationship("Book", back_populates="book_authors")
  author = relationship("Author", back_populates="book_authors")