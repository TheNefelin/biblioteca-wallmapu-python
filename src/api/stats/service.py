from sqlalchemy.orm import Session

from . import dtos, repository


def get_all_admin(db: Session) -> dtos.StatusAdminDTO:
  data = repository.get_all_admin(db)
  return dtos.StatusAdminDTO(**data)

