from uuid import UUID
from sqlalchemy.orm import Session

from . import dtos, repository

# -----------------------------------------------------------------
# GET ADMIN STATS 
def get_admin_stats(db: Session) -> dtos.AdminStatsDTO:
  data = repository.get_admin_stats(db)
  return dtos.AdminStatsDTO(**data)


# -----------------------------------------------------------------
# GET USER STATS
def get_user_stats(db: Session, user_id: UUID) -> dtos.UserStatsDTO:
  data = repository.get_user_stats(db, user_id)
  return dtos.UserStatsDTO(**data)

