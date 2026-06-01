from pydantic import BaseModel, ConfigDict

class NewsGalleryDTO(BaseModel): 
  id_news_gallery: int
  alt: str
  url: str
  news_id: int

  model_config = ConfigDict(from_attributes=True)
