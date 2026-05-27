from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreateFormatDTO(BaseModel):
  name: str
  
  model_config = ConfigDict(from_attributes=True)


class UpdateFormatDTO(CreateFormatDTO):
  id_format: int


class FormatDTO(UpdateFormatDTO):
  created_at: datetime
  updated_at: datetime
