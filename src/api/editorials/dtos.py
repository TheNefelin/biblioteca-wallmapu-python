from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreateEditorialDTO(BaseModel):
  name: str


class UpdateEditorialDTO(CreateEditorialDTO):
  id_editorial: int


class EditorialDTO(UpdateEditorialDTO):
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)