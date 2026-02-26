from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BookDTO(BaseModel):
  id_book: int
  title: str
  description: str
  cover_image_url: str
  isbn: str
  edition: str
  publication_year: int
  pages: int
  dewey_number: str
  cutter: str
  created_at: datetime
  updated_at: datetime
  editorial_id: int


  model_config = ConfigDict(from_attributes=True)

