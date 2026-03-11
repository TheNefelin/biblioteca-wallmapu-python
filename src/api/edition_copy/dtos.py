from datetime import datetime
from pydantic import BaseModel, ConfigDict

from src.api.edition_copy_status.dtos import CopyStatusDTO


class EditionCopyDTO(BaseModel):
  id_copy: int
  barcode: str
  signature_topography: str
  copy_number: int
  created_at: datetime
  updated_at: datetime
  edition_id: int
  status: CopyStatusDTO
  
  model_config = ConfigDict(from_attributes=True)