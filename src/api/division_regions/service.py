from sqlalchemy.orm import Session

from . import dtos, repository


def get_all(db: Session) -> list[dtos.RegionDTO]:
  items = repository.get_all(db)
  return [dtos.RegionDTO.model_validate(item) for item in items]

