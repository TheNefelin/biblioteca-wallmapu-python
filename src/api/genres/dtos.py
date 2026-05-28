from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreateGenreDTO(BaseModel):
  name: str


class UpdateGenreDTO(CreateGenreDTO):
  id_genre: int


class GenreDTO(UpdateGenreDTO):
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)

