from math import ceil
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models


# -----------------------------------------------------------------#
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  query = db.query(models.Genre)
  
  search_filter = pagination.search if pagination.search else None
  if search_filter:
    query = query.filter(
      func.unaccent(models.Genre.name).ilike(f"%{search_filter}%")
    )
  
  total_items = query.count()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
  
  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit
  
  result = (
    query
    .order_by(models.Genre.name.asc())
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
def get_all(db: Session) -> list[models.Genre]:
  return (
    db.query(models.Genre)
    .order_by(models.Genre.name.asc())
    .all()
  )


# -----------------------------------------------------------------#
# GET BY NAME
def get_by_name(db: Session, name: str) -> models.Genre | None:
  return (
    db.query(models.Genre)
    .filter(models.Genre.name.ilike(name))
    .first()
  )


# -----------------------------------------------------------------#
# CREATE
def create(db: Session, data: dict) -> models.Genre | None:
  item = models.Genre(**data)
  db.add(item)
  db.commit()
  db.refresh(item)
  
  return item


# -----------------------------------------------------------------#
# UPDATE
def update(db: Session, id: int, data: dict) -> models.Genre | None:
  item = (
    db.query(models.Genre)
    .filter(models.Genre.id_genre == id)
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
  from src.api.books import models as book_models
  
  relations = db.query(book_models.Book).filter(
    book_models.Book.genre_id == id
  ).first()
  
  if relations:
    return False
  
  item = (
    db.query(models.Genre)
    .filter(models.Genre.id_genre == id)
    .first()
  )
  
  if not item:
    return None
  
  db.delete(item)
  db.commit()
  
  return True
