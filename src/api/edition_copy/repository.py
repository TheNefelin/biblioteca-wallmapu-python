from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from src.api.editions import models as edition_models
from src.api.edition_copy_status import models as status_models
from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.EditionCopyDTO]:
  try:
    items = (
      db.query(models.EditionCopy)
      .options(
        joinedload(models.EditionCopy.status)
      )
      .order_by(models.EditionCopy.id_copy.asc())
      .all()
    )
    
    return [dtos.EditionCopyDTO.model_validate(item) for item in items]
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# GET BY ID
def get_by_id(id: int, db: Session) -> dtos.EditionCopyDTO:
  try:
    item = (
      db.query(models.EditionCopy)
      .options(
        joinedload(models.EditionCopy.status)
      )
      .filter(models.EditionCopy.id_copy == id)
      .first()
    )

    if not item:
      return None
    
    return dtos.EditionCopyDTO.model_validate(item)
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# GET BY EDITION ID
def get_by_edition_id(id: int, db: Session) -> list[dtos.EditionCopyDTO]:
  try:
    items = (
      db.query(models.EditionCopy)
      .options(
        joinedload(models.EditionCopy.status)
      )
      .filter(models.EditionCopy.edition_id == id)
      .order_by(models.EditionCopy.id_copy.asc())
      .all()
    )
    
    return [dtos.EditionCopyDTO.model_validate(item) for item in items]
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# CREATE
def create(data: dtos.CreateEditionCopyDTO, db: Session) -> dtos.EditionCopyDTO:
  try:
    edition = db.get(edition_models.Edition, data.edition_id)

    if not edition:
      raise ValueError("No se encontro la edición")

    status = db.get(status_models.CopyStatus, data.status_id)

    if not status:
      raise ValueError("No se encontro el estado")

    new_item = models.EditionCopy(**data.model_dump())
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return dtos.EditionCopyDTO.model_validate(new_item)
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------
# UPDATE
def update(id: int, data: dtos.UpdateEditionCopyDTO, db: Session) -> dtos.EditionCopyDTO:
  try:
    edition = db.get(edition_models.Edition, data.edition_id)

    if not edition:
      raise ValueError("No se encontro la edición")

    status = db.get(status_models.CopyStatus, data.status_id)

    if not status:
      raise ValueError("No se encontro el estado")

    item = (
      db.query(models.EditionCopy)
      .filter(models.EditionCopy.id_copy == id)
      .first()
    )

    if not item:
      return None

    update_item = data.model_dump(exclude_unset=True)
    for key, value in update_item.items():
      setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return dtos.EditionCopyDTO.model_validate(item)
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)  
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------
# DELETE
def delete(id: int, db: Session) -> bool:
  try:
    item = (
      db.query(models.EditionCopy)
      .filter(models.EditionCopy.id_copy == id)
      .first()
    )
    
    if not item:
      return False

    db.delete(item)
    db.commit()

    return True
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)
  except SQLAlchemyError as e:
    db.rollback()
    raise e  
  