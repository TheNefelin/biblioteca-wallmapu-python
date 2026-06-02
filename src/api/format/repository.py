from math import ceil
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models


# -----------------------------------------------------------------#
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  query = db.query(models.Format)
  
  search_filter = pagination.search if pagination.search else None
  if search_filter:
    query = query.filter(
      func.unaccent(models.Format.name).ilike(f"%{search_filter}%")
    )
  
  total_items = query.count()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
  
  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit
  
  result = (
    query
    .order_by(models.Format.name.asc())
    .offset(offset)
    .limit(pagination.limit)
    .all()
  )

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=result,
  )


# -----------------------------------------------------------------#
# GET ALL
def get_all(db: Session) -> list[models.Format]:
  return (
    db.query(models.Format)
    .order_by(models.Format.name.asc())
    .all()
  )


# -----------------------------------------------------------------#
# GET BY NAME
def get_by_name(db: Session, name: str) -> models.Format | None:
  return (
    db.query(models.Format)
    .filter(models.Format.name.ilike(name))
    .first()
  )


# -----------------------------------------------------------------#
# CREATE
def create(db: Session, data: dict) -> models.Format | None:
  item = models.Format(**data)
  db.add(item)
  db.commit()
  db.refresh(item)
  
  return item


# -----------------------------------------------------------------#
# UPDATE
def update(db: Session, id: int, data: dict) -> models.Format | None:
  item = (
    db.query(models.Format)
    .filter(models.Format.id_format == id)
    .first()
  )
  
  if not item:
    return None
  
  for key, value in data.items():
    setattr(item, key, value)
  
  db.commit()
  db.refresh(item)
  
  return item


# -----------------------------------------------------------------#
# DELETE
def delete(db: Session, id: int) -> bool | None:
  from src.api.edition_format import models as edition_format_models
  
  relations = db.query(edition_format_models.EditionFormat).filter(
    edition_format_models.EditionFormat.id_format == id
  ).first()
  
  if relations:
    return False
  
  item = (
    db.query(models.Format)
    .filter(models.Format.id_format == id)
    .first()
  )
  
  if not item:
    return None
  
  db.delete(item)
  db.commit()
  
  return True
