from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProvinceDTO(BaseModel):
  id_province: int
  province: str
  created_at: datetime
  updated_at: datetime
  region_id: int

  model_config = ConfigDict(from_attributes=True)
  