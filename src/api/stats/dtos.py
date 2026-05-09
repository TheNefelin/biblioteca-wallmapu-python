from pydantic import BaseModel, ConfigDict


class AdminStatsDTO(BaseModel):
  reservations: int
  loans: int
  books: int
  users: int
  news: int

  model_config = ConfigDict(from_attributes=True)


class UserStatsDTO(BaseModel):
  total_borrowed: int
  active_loans: int
  overdue_loans: int

  model_config = ConfigDict(from_attributes=True)
  