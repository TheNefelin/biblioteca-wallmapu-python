from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from src.api.copy_status import models as copy_status_models
from src.api.editions.models import Edition
from src.api.editorials.models import Editorial
from . import models



# -----------------------------------------------------------------
# GET ALL DETAIL (una sola query, solo columnas del DTO)
def _build_detail_query(db: Session):
  return (
    db.query(
      models.Copy.id_copy,
      models.Copy.barcode,
      models.Copy.signature_topography,
      models.Copy.copy_number,
      models.Copy.created_at,
      models.Copy.updated_at,
      models.Copy.status_id,
      copy_status_models.CopyStatus.name.label("status_name"),
      models.Copy.edition_id,
      Edition.edition.label("edition_name"),
      Edition.isbn.label("edition_isbn"),
      Edition.cover_image.label("edition_cover_image"),
      func.coalesce(Editorial.id_editorial, 0).label("editorial_id"),
      func.coalesce(Editorial.name, "Sin Editorial").label("editorial_name"),
    )
    .join(copy_status_models.CopyStatus, models.Copy.status_id == copy_status_models.CopyStatus.id_status)
    .join(Edition, models.Copy.edition_id == Edition.id_edition)
    .outerjoin(Editorial, Edition.editorial_id == Editorial.id_editorial)
  )


def get_all_detail_by_edition_id(db: Session, edition_id: int) -> list:
  return (
    _build_detail_query(db)
    .filter(models.Copy.edition_id == edition_id)
    .order_by(models.Copy.id_copy.asc())
    .all()
  )


def get_all_detail_by_book_id(db: Session, book_id: int) -> list:
  return (
    _build_detail_query(db)
    .filter(Edition.book_id == book_id)
    .order_by(models.Copy.id_copy.asc())
    .all()
  )


# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Copy]:
  return (
    db.query(models.Copy)
    .options(joinedload(models.Copy.status))
    .order_by(models.Copy.id_copy.asc())
    .all()
  )


# -----------------------------------------------------------------
# GET BY ID
def get_by_id(db: Session, id: int) -> models.Copy | None:
  return (
    db.query(models.Copy)
    .options(joinedload(models.Copy.status))
    .filter(models.Copy.id_copy == id)
    .first()
  )


# -----------------------------------------------------------------
# GET BY EDITION ID
def get_by_edition_id(db: Session, id: int) -> list[models.Copy]:
  return (
    db.query(models.Copy)
    .options(joinedload(models.Copy.status))
    .filter(models.Copy.edition_id == id)
    .order_by(models.Copy.id_copy.asc())
    .all()
  )


# -----------------------------------------------------------------
# CHECK IF SIGNATURE EXISTS
def signature_exists(db: Session, signature: str, exclude_id: int = 0) -> bool:
  query = db.query(models.Copy.signature_topography).filter(
    models.Copy.signature_topography == signature
  )
  if exclude_id > 0:
    query = query.filter(models.Copy.id_copy != exclude_id)
  return query.first() is not None


# -----------------------------------------------------------------
# CHECK IF COPY NUMBER EXISTS FOR EDITION
def copy_number_exists(db: Session, edition_id: int, copy_number: int, exclude_id: int = 0) -> bool:
  query = db.query(models.Copy.copy_number).filter(
    models.Copy.edition_id == edition_id,
    models.Copy.copy_number == copy_number
  )
  if exclude_id > 0:
    query = query.filter(models.Copy.id_copy != exclude_id)
  return query.first() is not None


# -----------------------------------------------------------------
# CREATE
def create(db: Session, data: dict) -> models.Copy:
  item = models.Copy(**data)
  db.add(item)
  db.commit()
  db.refresh(item)
  return item


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, item: models.Copy, data: dict) -> models.Copy:
  for key, value in data.items():
    setattr(item, key, value)
  db.commit()
  db.refresh(item)
  return item


# -----------------------------------------------------------------
# GET BY BOOK ID AND STATUS (with edition and editorial)
def get_by_book_id_and_status(db: Session, book_id: int, status_id: int) -> list[models.Copy]:
  from src.api.editions.models import Edition

  return (
    db.query(models.Copy)
    .options(
      joinedload(models.Copy.status),
      joinedload(models.Copy.edition).joinedload(Edition.editorial)
    )
    .join(Edition)
    .filter(
      Edition.book_id == book_id,
      models.Copy.status_id == status_id
    )
    .order_by(Edition.id_edition.asc(), models.Copy.id_copy.asc())
    .all()
  )


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, item: models.Copy) -> None:
  db.delete(item)
  db.commit()
