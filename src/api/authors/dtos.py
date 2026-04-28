from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreateAuthorDTO(BaseModel):
  name: str

  model_config = ConfigDict(from_attributes=True)


class UpdateAuthorDTO(CreateAuthorDTO):
  id_author: int


class AuthorDTO(UpdateAuthorDTO):
  created_at: datetime
  updated_at: datetime

