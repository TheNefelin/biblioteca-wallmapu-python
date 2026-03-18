from sqlalchemy.orm import Session

from . import dtos, repository


def get_all(db: Session) -> list[dtos.EditorialDTO]:
  items = repository.get_all(db)
  return [dtos.EditorialDTO.model_validate(item) for item in items]

