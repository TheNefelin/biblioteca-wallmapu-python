from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from src.api.authors.dtos import AuthorDTO
from src.api.subjects.dtos import SubjectDTO
from src.api.genres.dtos import GenreDTO


class CreateBookDTO(BaseModel):
  title: str
  summary: str
  genre_id: int
  author_ids: List[int]
  subject_ids: List[int]

  model_config = ConfigDict(from_attributes=True)


class UpdateBookDTO(CreateBookDTO):
  id_book: int


class BookDTO(BaseModel):
  id_book: int
  title: str
  summary: str
  created_at: datetime
  updated_at: datetime
  genre: GenreDTO
  authors: List[AuthorDTO]
  subjects: List[SubjectDTO]

  model_config = ConfigDict(from_attributes=True)


class BookDetailDTO(BaseModel):
  id_book: int
  title: str
  created_at: datetime
  updated_at: datetime
  genre_id: int
  genre_name: str
  author_id: Optional[int]
  author_name: Optional[str]
  edition_cover_image: Optional[str]
  edition_count: int
  copy_count: int

  model_config = ConfigDict(from_attributes=True)
