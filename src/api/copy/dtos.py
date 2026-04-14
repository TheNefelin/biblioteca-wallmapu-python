from calendar import c
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


class CopyWithStatusDTO(UpdateCopyDTO):
  id_copy: int
  signature_topography: str
  edition_id: int
  copy_number: int
  barcode: str  
  created_at: datetime
  updated_at: datetime
  status: CopyStatusDTO  

  model_config = ConfigDict(from_attributes=True)
