from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreateSubjectDTO(BaseModel):
  name: str


class UpdateSubjectDTO(CreateSubjectDTO):
  id_subject: int


class SubjectDTO(UpdateSubjectDTO):
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)


