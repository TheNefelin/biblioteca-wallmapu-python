from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from src.api.copy_status.dtos import CopyStatusDTO


class CreateCopyDTO(BaseModel):
  signature_topography: str
  copy_number: int
  edition_id: int
  status_id: int

  model_config = ConfigDict(from_attributes=True)


class UpdateCopyDTO(CreateCopyDTO):
  id_copy: int


class CopyDTO(UpdateCopyDTO):
  created_at: datetime
  updated_at: datetime


class CopyForEditionDTO(BaseModel):
  id_copy: int
  barcode: str
  signature_topography: str
  copy_number: str
  edition_id: int
  created_at: datetime
  updated_at: datetime
  status: CopyStatusDTO
  status_id: int
  availability_status: Optional[str] = None
  
  model_config = ConfigDict(from_attributes=True)


class EditionBasicDTO(BaseModel):
  id_edition: int
  edition: str
  isbn: str
  publication_year: int
  pages: int
  cover_image: Optional[str]
  editorial_id: int
  editorial_name: str

  model_config = ConfigDict(from_attributes=True)


class CopyWithAvailabilityDTO(BaseModel):
  id_copy: int
  barcode: str
  signature_topography: str
  copy_number: str
  edition_id: int
  edition: EditionBasicDTO
  availability_status: str

  model_config = ConfigDict(from_attributes=True)
