from sqlalchemy.orm import Session

from . import dtos, repository


def get_all(db: Session) -> list[dtos.ProvinceDTO]:
  items = repository.get_all(db)
  return [dtos.ProvinceDTO.model_validate(item) for item in items]

