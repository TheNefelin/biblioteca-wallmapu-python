from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from src.api.book_authors.dtos import AuthorDTO
from src.api.book_genres.dtos import GenreDTO
from src.api.book_subjects.dtos import SubjectDTO
from src.api.editorials.dtos import EditorialDTO
from src.api.edition_copy.dtos import EditionCopyDTO


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


class EditionDetailDTO(BaseModel):
  id_edition: int
  edition: str
  isbn: str
  publication_year: int
  pages: int
  cover_image: Optional[str]
  created_at: datetime
  updated_at: datetime
  editorial: EditorialDTO
  copies: List[EditionCopyDTO]
  book: BookForEditionDTO

  model_config = ConfigDict(from_attributes=True)


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
