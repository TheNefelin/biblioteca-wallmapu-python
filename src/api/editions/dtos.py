from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EditionDTO(BaseModel):
  id_edition: int
  edition: str
  isbn: str
  publication_year: int
  pages: int
  cover_image: str
  created_at: datetime
  updated_at: datetime
  book_id: int

  model_config = ConfigDict(from_attributes=True)

class CreateEditionDTO(BaseModel):
  edition: str
  isbn: str
  publication_year: int
  pages: int
  cover_image: str
  book_id: int

  model_config = ConfigDict(from_attributes=True)

class UpdateEditionDTO(BaseModel):
  id_edition: int
  edition: str
  isbn: str
  publication_year: int
  pages: int
  cover_image: str
  book_id: int

  model_config = ConfigDict(from_attributes=True)
