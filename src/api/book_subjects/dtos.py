from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SubjectDTO(BaseModel):
  id_subject: int
  subject: str
  created_at: datetime
  updated_at: datetime
  
  model_config = ConfigDict(from_attributes=True)

