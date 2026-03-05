from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict

from src.api.book_authors.dtos import AuthorDTO
from src.api.book_subjects.dtos import SubjectDTO
from src.api.book_genres.dtos import BookGenreDTO


class BookDTO(BaseModel):
  id_book: int
  title: str
  summary: str
  created_at: datetime
  updated_at: datetime
  genre: BookGenreDTO
  authors: List[AuthorDTO]
  subjects: List[SubjectDTO]

  model_config = ConfigDict(from_attributes=True)
