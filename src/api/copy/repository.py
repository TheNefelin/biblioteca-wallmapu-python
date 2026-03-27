from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from . import models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Copy]:
  try:
    return (
      db.query(models.Copy)
      .options(
        joinedload(models.Copy.status)
      )
      .order_by(models.Copy.id_copy.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# GET BY ID
def get_by_id(id: int, db: Session) -> models.Copy | None:
  try:
    item = (
      db.query(models.Copy)
      .options(
        joinedload(models.Copy.status)
      )
      .filter(models.Copy.id_copy == id)
      .first()
    )

    if not item:
      return None
    
    return item
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# GET BY EDITION ID
def get_by_edition_id(id: int, db: Session) -> list[models.Copy]:
  try:
    items = (
      db.query(models.Copy)
      .options(
        joinedload(models.Copy.status)
      )
      .filter(models.Copy.edition_id == id)
      .order_by(models.Copy.id_copy.asc())
      .all()
    )
    return items
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# CREATE
def create(data: dict, db: Session) -> models.Copy:
  try:
    new_item = models.Copy(**data)
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------
# UPDATE
def update(id: int, data: dict, db: Session) -> models.Copy | None:
  try:
    item = (
      db.query(models.Copy)
      .filter(models.Copy.id_copy == id)
      .first()
    )

    if not item:
      return None

    for key, value in data.items():
      setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)  
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------
# GET BY BOOK ID AND STATUS
def get_by_book_id_and_status(db: Session, book_id: int, status_id: int) -> list[models.Copy]:
  try:
    from src.api.editions.models import Edition
    items = (
      db.query(models.Copy)
      .options(
        joinedload(models.Copy.status)
      )
      .join(Edition)
      .filter(
        Edition.book_id == book_id,
        models.Copy.status_id == status_id
      )
      .order_by(models.Copy.id_copy.asc())
      .all()
    )
    return items
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# DELETE
def delete(id: int, db: Session) -> bool:
  try:
    item = (
      db.query(models.Copy)
      .filter(models.Copy.id_copy == id)
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
  