from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from src.api.edition_copy import models as edition_copy_models
from . import models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Edition]:
  stmt = (
    select(models.Edition)
    .options(
      joinedload(models.Edition.editorial),
      joinedload(models.Edition.book),
      joinedload(models.Edition.copies),
    )
    .order_by(models.Edition.edition.asc())
  )

  #return db.scalars(stmt).all()
  return db.scalars(stmt).unique().all()


# -----------------------------------------------------------------
# GET BY ID
def get_by_id(id: int, db: Session) -> models.Edition | None:
  stmt = (
    select(models.Edition)
    .options(
      joinedload(models.Edition.editorial),
      joinedload(models.Edition.book),
      joinedload(models.Edition.copies),
    )
    .where(models.Edition.id_edition == id)
  )

  return db.scalars(stmt).first()


# -----------------------------------------------------------------
# GET ENTITY BY ID (sin joins)
def get_entity_by_id(id: int, db: Session) -> models.Edition | None:
  return db.get(models.Edition, id)


# -----------------------------------------------------------------
# CREATE
def create(data: dict, db: Session) -> models.Edition:
  try:
    new_item = models.Edition(**data)
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item
  except IntegrityError as e:
    db.rollback()
    raise ValueError(f"Violación de integridad: {e.orig}")
  except SQLAlchemyError as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# UPDATE
def update(item: models.Edition, data: dict, db: Session) -> models.Edition:
  try:
    for key, value in data.items():
      setattr(item, key, value)
    
    db.commit()
    db.refresh(item)

    return item
  except IntegrityError as e:
    db.rollback()
    raise ValueError(f"Violación de integridad: {e.orig}")
  except SQLAlchemyError as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# DELETE
def delete(edition: models.Edition, db: Session) -> str | None:
  try:
    # Validar dependencias
    has_copies = (
      db.query(edition_copy_models.EditionCopy)
      .filter(edition_copy_models.EditionCopy.edition_id == edition.id_edition)
      .first()
    )
    if has_copies:
      raise ValueError(f"El Ejemplar ({edition.edition}) tiene copias asociados")

    url = edition.cover_image
    db.delete(edition)
    db.commit()
    
    return url
  except SQLAlchemyError as e:
    db.rollback()
    raise e
