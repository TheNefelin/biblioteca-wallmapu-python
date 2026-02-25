from datetime import datetime
from pydantic import BaseModel, ConfigDict

class RegionDTO(BaseModel):
  id_region: int
  region: str
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)
  