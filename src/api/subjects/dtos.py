from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CreateSubjectDTO(BaseModel):
  name: str
  
  model_config = ConfigDict(from_attributes=True)


class UpdateSubjectDTO(CreateSubjectDTO):
  id_subject: int
  

class SubjectDTO(UpdateSubjectDTO):
  created_at: datetime
  updated_at: datetime


