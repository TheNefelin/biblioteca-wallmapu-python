from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from src.api.editions.dtos import EditionWithEditorialDTO
from src.api.copy_status.dtos import CopyStatusDTO


class CopyAvailabilityDTO(BaseModel):
  id_copy: int
  signature_topography: str
  edition_id: int
  copy_number: int
  barcode: str  
  created_at: datetime
  updated_at: datetime
  status: CopyStatusDTO
  edition: EditionWithEditorialDTO
  availability_status: Optional[str] = None

  model_config = ConfigDict(from_attributes=True)
