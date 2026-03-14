from datetime import datetime
from pydantic import BaseModel, ConfigDict

from src.api.edition_copy_status.dtos import CopyStatusDTO


class CreateEditionCopyDTO(BaseModel):
  signature_topography: str
  copy_number: int
  edition_id: int
  status_id: int

  model_config = ConfigDict(from_attributes=True)


class UpdateEditionCopyDTO(CreateEditionCopyDTO):
  id_copy: int


class EditionCopyDTO(BaseModel):
  id_copy: int
  barcode: str
  signature_topography: str
  copy_number: int
  edition_id: int
  created_at: datetime
  updated_at: datetime
  status: CopyStatusDTO
  
  model_config = ConfigDict(from_attributes=True)
