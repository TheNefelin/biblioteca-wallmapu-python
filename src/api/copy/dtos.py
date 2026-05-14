from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from src.api.copy_status.dtos import CopyStatusDTO


class CreateCopyDTO(BaseModel):
  signature_topography: str
  edition_id: int
  copy_number: int

  model_config = ConfigDict(from_attributes=True)


class UpdateCopyDTO(CreateCopyDTO):
  id_copy: int
  status_id: int


class CopyDTO(UpdateCopyDTO):
  barcode: str  
  created_at: datetime
  updated_at: datetime


class CopyDetailDTO(BaseModel):
  id_copy: int  
  barcode: str
  signature_topography: str
  copy_number: int
  created_at: datetime
  updated_at: datetime
  status_id: int
  status_name: str
  edition_id: int
  edition_name: str
  edition_isbn: str
  edition_cover_image: Optional[str] = None
  editorial_id: int
  editorial_name: str  
  is_availability: bool
  availability_status: str
  
  model_config = ConfigDict(from_attributes=True)
