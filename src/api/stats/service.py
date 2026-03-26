from sqlalchemy.orm import Session

from . import dtos, repository

# -----------------------------------------------------------------
# GET ADMIN STATS 
def get_admin_stats(db: Session) -> dtos.AdminStatsDTO:
  data = repository.get_admin_stats(db)
  return dtos.AdminStatsDTO(**data)



def get_all_admin(db: Session) -> dtos.StatusAdminDTO:
  data = repository.get_all_admin(db)
  return dtos.StatusAdminDTO(**data)

