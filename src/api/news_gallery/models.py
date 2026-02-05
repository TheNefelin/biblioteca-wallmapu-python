from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from src.core.database import Base

class NewsGallery(Base):
  __tablename__ = "wm_news_gallery"

  id_news_gallery = Column(Integer, primary_key=True, autoincrement=True)
  alt = Column(String(45), nullable=False)
  img = Column(String(255), nullable=False)
  news_id = Column(Integer, ForeignKey('wm_news.id_news'))

  news = relationship("News", back_populates="images")