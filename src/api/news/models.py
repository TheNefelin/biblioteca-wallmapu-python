from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.orm import relationship
from src.core.database import Base

class News(Base):
  __tablename__ = "wm_news"

  id_news = Column(Integer, primary_key=True, autoincrement=True)
  title = Column(String(45), nullable=False)
  subtitle = Column(String(256), nullable=False)
  body = Column(Text, nullable=False)  # Use Text for longer content
  created_at = Column(DateTime, server_default=func.now())
  updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

  # Relationship with gallery images
  images = relationship("NewsGallery", back_populates="news")
  