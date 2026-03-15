from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from src.api.edition_copy.dtos import EditionCopyDTO
from src.api.editorials.dtos import EditorialDTO
from src.api.book_authors.dtos import AuthorDTO
from src.api.book_subjects.dtos import SubjectDTO
from src.api.book_genres.dtos import GenreDTO


class EditionForBookDTO(BaseModel):
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

  model_config = ConfigDict(from_attributes=True)


class BookDetailDTO(BaseModel):
  id_book: int
  title: str
  summary: str
  created_at: datetime
  updated_at: datetime
  genre: GenreDTO
  authors: List[AuthorDTO]
  subjects: List[SubjectDTO]
  editions: List[EditionForBookDTO]

  model_config = ConfigDict(from_attributes=True)


class CreateBookDTO(BaseModel):
  title: str
  summary: str
  genre_id: int
  author_ids: List[int]
  subject_ids: List[int]


class UpdateBookDTO(CreateBookDTO):
  id_book: int


class BookDTO(UpdateBookDTO):
    created_at: datetime
    updated_at: datetime
