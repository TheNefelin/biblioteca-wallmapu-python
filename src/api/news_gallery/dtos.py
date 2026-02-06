from typing import Optional
from pydantic import BaseModel, ConfigDict, computed_field

class CreateGalleryDTO(BaseModel): 
  alt: str
  img: str
  news_id: int

class NewsGalleryDTO(BaseModel): 
  id_news_gallery: int
  alt: str
  img: str
  news_id: int

  model_config = ConfigDict(from_attributes=True)
