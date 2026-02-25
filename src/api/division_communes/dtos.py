from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CommuneDTO(BaseModel):
  id_commune: int
  commune: str
  created_at: datetime
  updated_at: datetime
  province_id: int

  model_config = ConfigDict(from_attributes=True)
  