from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CreateNewsDTO(BaseModel): 
  title: str
  subtitle: str
  body: str

class UpdateNewsDTO(BaseModel): 
  id_news: int
  title: str
  subtitle: str
  body: str

class NewsDTO(BaseModel): 
  id_news: int
  title: str
  subtitle: str
  body: str
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)
