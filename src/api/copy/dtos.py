from datetime import datetime
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
  copy_number: int
  edition_id: int
  created_at: datetime
  updated_at: datetime
  status: CopyStatusDTO
  
  model_config = ConfigDict(from_attributes=True)
