from contextvars import ContextVar
from pydantic import BaseModel, ConfigDict, computed_field

# Variable de contexto para almacenar la URL base
base_url_context: ContextVar[str] = ContextVar('base_url', default='')

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

  @computed_field
  @property
  def url(self) -> str:
    """Genera la URL completa de la imagen con dominio"""
    base_url = base_url_context.get()
    if base_url:
      return f"{base_url}/static/news/{self.img}"
    # Fallback si no hay base_url
    return f"/static/news/{self.img}"
