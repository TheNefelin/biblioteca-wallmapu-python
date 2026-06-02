import unicodedata
from datetime import datetime
from math import ceil
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  query = db.query(models.Editorial)

  search = pagination.search.strip() if pagination.search else ""
  if search:
    search_norm = unicodedata.normalize('NFKD', search).encode('ascii', 'ignore').decode('ascii')
    query = query.filter(func.unaccent(models.Editorial.name).ilike(f"%{search_norm}%"))

  total_items = query.count()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0

  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  items = query.order_by(models.Editorial.name.asc()).offset(offset).limit(pagination.limit).all()

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=items,
  )


# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Editorial]:
  return (
    db.query(models.Editorial)
    .order_by(models.Editorial.name.asc())
    .all()
  )


# -----------------------------------------------------------------
# GET BY ID
def get_by_id(db: Session, id: int) -> models.Editorial | None:
  return db.query(models.Editorial).filter(models.Editorial.id_editorial == id).first()


# -----------------------------------------------------------------
# EXISTS BY NAME
def exists_by_name(db: Session, name: str, exclude_id: int | None = None) -> bool:
  query = db.query(models.Editorial).filter(models.Editorial.name.ilike(name))
  if exclude_id:
    query = query.filter(models.Editorial.id_editorial != exclude_id)
  return query.first() is not None


# -----------------------------------------------------------------
# CREATE
def create(db: Session, data: dict) -> models.Editorial:
  entity = models.Editorial(**data)
  db.add(entity)
  db.commit()
  db.refresh(entity)
  return entity


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, entity: models.Editorial, update_data: dict) -> models.Editorial:
  for key, value in update_data.items():
    setattr(entity, key, value)
  entity.updated_at = datetime.now()
  db.commit()
  db.refresh(entity)
  return entity


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, entity: models.Editorial) -> None:
  db.delete(entity)
  db.commit()


# -----------------------------------------------------------------
# EXISTS BY ID
def exists_by_id(db: Session, id: int) -> bool:
  return db.query(models.Editorial).filter(models.Editorial.id_editorial == id).first() is not None