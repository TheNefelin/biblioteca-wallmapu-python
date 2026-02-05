from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict

from src.api.news_gallery.dtos import NewsGalleryDTO

class CreateNewsDTO(BaseModel): 
  title: str
  subtitle: str
  body: str

class UpdateNewsDTO(BaseModel): 
  id_news: int
  title: str
  subtitle: str
  body: str

class NewsDTO(BaseModel): 
  id_news: int
  title: str
  subtitle: str
  body: str
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)

class NewsWithGalleryDTO(BaseModel):
  id_news: int
  title: str
  subtitle: str
  body: str
  created_at: datetime
  updated_at: datetime
  images: List[NewsGalleryDTO]  # Relación con las imágenes
  
  model_config = ConfigDict(from_attributes=True)