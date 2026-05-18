from math import ceil
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  query = db.query(models.Subject)
  
  search_filter = pagination.search if pagination.search else None
  if search_filter:
    query = query.filter(
      models.Subject.name.ilike(f"%{search_filter}%")
    )
  
  total_items = query.count()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
  
  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit
  
  result = (
    query
    .order_by(models.Subject.name.asc())
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


# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Subject]:
  return (
    db.query(models.Subject)
    .order_by(models.Subject.name.asc())
    .all()
  )


# -----------------------------------------------------------------
# CREATE
def create(db: Session, data: dict) -> models.Subject | None:
  item = models.Subject(**data)
  db.add(item)
  db.commit()
  db.refresh(item)
  
  return item


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, id: int, data: dict) -> models.Subject | None:
  item = (
    db.query(models.Subject)
    .filter(models.Subject.id_subject == id)
    .first()
  )
  
  if not item:
    return None
  
  for key, value in data.items():
    setattr(item, key, value)
  
  db.commit()
  db.refresh(item)
  
  return item


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, id: int) -> bool | None:
  from src.api.book_subjects import models as book_subject_models
  
  relations = db.query(book_subject_models.BookSubject).filter(
    book_subject_models.BookSubject.id_subject == id
  ).first()
  
  if relations:
    return False
  
  item = (
    db.query(models.Subject)
    .filter(models.Subject.id_subject == id)
    .first()
  )
  
  if not item:
    return None
  
  db.delete(item)
  db.commit()
  
  return True
