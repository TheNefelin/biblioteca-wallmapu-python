from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreateGenreDTO(BaseModel):
  name: str
  
  model_config = ConfigDict(from_attributes=True)


class UpdateGenreDTO(CreateGenreDTO):
  id_genre: int


class GenreDTO(UpdateGenreDTO):
  created_at: datetime
  updated_at: datetime

