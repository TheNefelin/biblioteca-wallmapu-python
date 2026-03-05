from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from src.core.database import Base


class Author(Base):
  __tablename__ = "wm_authors"

  id_author = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(200), nullable=False)
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
  
  book_authors = relationship("BookAuthor", back_populates="author")
