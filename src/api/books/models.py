from sqlalchemy import Column, DateTime, Integer, String, Text, func
from src.core.database import Base


class Book(Base):
  __tablename__ = "wm_books"

  id_book = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String(300), nullable=False)
  description = Column(Text, nullable=False)
  cover_image_url = Column(String(256), nullable=False)
  isbn = Column(String(20), nullable=False)
  edition = Column(String(50), nullable=False)
  publication_year = Column(Integer, nullable=False)
  pages = Column(Integer, nullable=True)
  dewey_number = Column(String(20), nullable=False)
  cutter = Column(String(20), nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
  editorial_id = Column(Integer, nullable=True)
