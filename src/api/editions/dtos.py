from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from src.api.authors.dtos import AuthorDTO
from src.api.genres.dtos import GenreDTO
from src.api.subjects.dtos import SubjectDTO



class CreateEditionDTO(BaseModel):
  edition: str
  isbn: str
  publication_year: int
  pages: int
  cover_image: Optional[str]
  editorial_id: int
  book_id: int

  model_config = ConfigDict(from_attributes=True)


class UpdateEditionDTO(CreateEditionDTO):
  id_edition: int


class EditionDTO(UpdateEditionDTO):
  created_at: datetime
  updated_at: datetime


class EditionDetailDTO(BaseModel):
  id_edition: int
  edition: str
  isbn: str
  publication_year: int
  pages: int
  cover_image: Optional[str]
  created_at: datetime
  updated_at: datetime
  editorial_id: int
  editorial_name: str
  book_id: int
  book_title: str
  genre_id: int
  genre_name: str
  author_id: Optional[int]
  author_name: Optional[str]
  copy_count: int

  model_config = ConfigDict(from_attributes=True)


#---------------------------------------

class BookForEditionDTO(BaseModel):
  id_book: int
  title: str
  summary: str
  created_at: datetime
  updated_at: datetime  
  genre: GenreDTO
  authors: List[AuthorDTO]
  subjects: List[SubjectDTO]

  model_config = ConfigDict(from_attributes=True)


