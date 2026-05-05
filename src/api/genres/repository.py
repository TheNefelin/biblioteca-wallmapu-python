from math import ceil
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
      models.Genre.name.ilike(f"%{search_filter}%")
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
  
  next_url = f"/api/genre/pagination?page={page + 1}&limit={pagination.limit}" if page < total_pages else None
  prev_url = f"/api/genre/pagination?page={page - 1}&limit={pagination.limit}" if page > 1 else None
  
  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=result,
    next=next_url,
    prev=prev_url
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
