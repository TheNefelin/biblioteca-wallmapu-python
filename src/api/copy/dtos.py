from datetime import datetime
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


class CopyMinimalDTO(BaseModel):
  id_copy: int
  edition_id: int
  signature_topography: str
  barcode: str

  model_config = ConfigDict(from_attributes=True)


class CopyWithStatusDTO(BaseModel):
  id_copy: int
  signature_topography: str
  edition_id: int
  copy_number: int
  barcode: str  
  created_at: datetime
  updated_at: datetime
  status: CopyStatusDTO  

  model_config = ConfigDict(from_attributes=True)
