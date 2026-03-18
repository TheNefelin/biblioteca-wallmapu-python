from datetime import datetime
from pydantic import BaseModel, ConfigDict


class GenreDTO(BaseModel):
  id_genre: int
  name: str
  created_at: datetime
  updated_at: datetime
  
  model_config = ConfigDict(from_attributes=True)

