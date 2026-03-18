from sqlalchemy.orm import Session

from src.api.copy_status import models as status_models
from src.api.editions import models as edition_models
from . import dtos, models, repository


def get_all(db: Session) -> list[dtos.CopyDTO]:
  items = repository.get_all(db)
  return [dtos.CopyDTO.model_validate(item) for item in items]


def get_by_id(id: int, db: Session) -> dtos.CopyDTO | None:
  item = repository.get_by_id(id, db)
  if not item:
    return None
  return dtos.CopyDTO.model_validate(item)


def get_by_edition_id(id_edition: int, db: Session) -> list[dtos.CopyDTO]:
  items = repository.get_by_edition_id(id_edition, db)
  return [dtos.CopyDTO.model_validate(item) for item in items]


def create(data: dtos.CreateCopyDTO, db: Session) -> dtos.CopyDTO:
  if not db.get(edition_models.Edition, data.edition_id):
    raise ValueError("No se encontro la edición")
  if not db.get(status_models.CopyStatus, data.status_id):
    raise ValueError("No se encontro el estado")

  entity = repository.create(data.model_dump(), db)
  return dtos.CopyDTO.model_validate(entity)


def update(id: int, data: dtos.UpdateCopyDTO, db: Session) -> dtos.CopyDTO | None:
  if not db.get(edition_models.Edition, data.edition_id):
    raise ValueError("No se encontro la edición")
  if not db.get(status_models.CopyStatus, data.status_id):
    raise ValueError("No se encontro el estado")

  entity = repository.update(id, data.model_dump(exclude_unset=True), db)
  if not entity:
    return None
  return dtos.CopyDTO.model_validate(entity)


def delete(id: int, db: Session) -> bool:
  return repository.delete(id, db)

