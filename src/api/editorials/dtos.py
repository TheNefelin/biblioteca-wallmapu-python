from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EditorialDTO(BaseModel):
  id_editorial: int
  editorial: str
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)

