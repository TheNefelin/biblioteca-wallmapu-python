from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from src.api.format.dtos import FormatDTO


class CreateEditionDTO(BaseModel):
  edition: Optional[str] = None
  isbn: Optional[str] = None
  publication_year: int
  pages: int
  cover_image: Optional[str] = None
  editorial_id: int
  book_id: int
  format_ids: Optional[list[int]] = None


class UpdateEditionDTO(CreateEditionDTO):
  id_edition: int


class EditionDTO(BaseModel):
  id_edition: int
  edition: Optional[str]
  isbn: Optional[str]
  publication_year: int
  pages: int
  cover_image: Optional[str]
  editorial_id: int
  book_id: int
  created_at: datetime
  updated_at: datetime
  formats: List[FormatDTO]

  model_config = ConfigDict(from_attributes=True)


class EditionFilterDTO(BaseModel):
  id_author: Optional[int] = Field(None, description="Filtrar por autor")
  id_editorial: Optional[int] = Field(None, description="Filtrar por editorial")
  id_genre: Optional[int] = Field(None, description="Filtrar por género")
  id_format: Optional[int] = Field(None, description="Filtrar por formato")
  id_subject: Optional[int] = Field(None, description="Filtrar por descriptores")


class EditionDetailDTO(BaseModel):
  id_edition: int
  edition: Optional[str]
  isbn: Optional[str]
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
