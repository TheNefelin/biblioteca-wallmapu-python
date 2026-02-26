from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EditorialDTO(BaseModel):
  id_editorial: int
  name: str
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)

