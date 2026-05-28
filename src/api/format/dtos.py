from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreateFormatDTO(BaseModel):
  name: str


class UpdateFormatDTO(CreateFormatDTO):
  id_format: int


class FormatDTO(UpdateFormatDTO):
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)
