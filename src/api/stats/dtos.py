from pydantic import BaseModel, ConfigDict


class AdminStatsDTO(BaseModel):
  reservations: int
  loans: int
  books: int
  users: int
  news: int

  model_config = ConfigDict(from_attributes=True)


class StatusAdminDTO(BaseModel):
  users: int
  news: int
  regions: int
  provinces: int
  communes: int
  authors: int
  editorials: int
  subjects: int = 0 
  books: int = 0

  model_config = ConfigDict(from_attributes=True)
  