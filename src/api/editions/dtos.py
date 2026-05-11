from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

from src.api.authors.dtos import AuthorDTO
from src.api.genres.dtos import GenreDTO
from src.api.subjects.dtos import SubjectDTO
from src.api.editorials.dtos import EditorialDTO
from src.api.copy.dtos import CopyWithStatusDTO


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


# -------------------------------------------------

class EditionMinimalDTO(BaseModel):
  id_edition: int
  book_id: int
  edition: str
  isbn: str

  model_config = ConfigDict(from_attributes=True)

class EditionWithEditorialDTO(BaseModel):
  id_edition: int
  edition: str
  isbn: str
  publication_year: int
  pages: int
  cover_image: Optional[str]
  book_id: int
  editorial: EditorialDTO
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)
    
    
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
  copies: List[CopyWithStatusDTO]
  book: BookForEditionDTO

  model_config = ConfigDict(from_attributes=True)
