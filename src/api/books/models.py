from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from src.core.database import Base

class Book(Base):
  __tablename__ = "wm_books"

  id_book = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String(200), nullable=False)
  summary = Column(Text, nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

  genre_id = Column(Integer, ForeignKey('wm_genres.id_genre'))
  genre = relationship("Genre", back_populates="books")

  book_authors = relationship("BookAuthor", back_populates="book")
  book_subjects = relationship("BookSubject", back_populates="book")

  editions = relationship("Edition", back_populates="book")

  @property
  def authors(self): return [ba.author for ba in self.book_authors]

  @property
  def subjects(self): return [bs.subject for bs in self.book_subjects]


class BookAuthor(Base):
  __tablename__ = "wm_book_author"

  id_author = Column(Integer, ForeignKey("wm_authors.id_author"), primary_key=True)
  id_book = Column(Integer, ForeignKey("wm_books.id_book"), primary_key=True)
  created_at = Column(DateTime, server_default=func.now())

  book = relationship("Book", back_populates="book_authors")
  author = relationship("Author", back_populates="book_authors")


