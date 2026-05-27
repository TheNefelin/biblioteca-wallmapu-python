from math import ceil
from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models


# -----------------------------------------------------------------
# GET ALL Pagination
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  query = (
    db.query(models.News)
    .options(joinedload(models.News.images))
  )
  
  if pagination.search:
    query = query.filter(
      or_(
        models.News.title.ilike(f"%{pagination.search}%"),
        models.News.subtitle.ilike(f"%{pagination.search}%")
      )
    )
  
  items = query.count()
  pages = ceil(items / pagination.limit) if items > 0 else 0

  page = min(pagination.page, pages) if pages > 0 else 1
  skip = (page - 1) * pagination.limit

  result = (
    query
    .order_by(models.News.created_at.desc()) #.order_by(func.random())
    .offset(skip)
    .limit(pagination.limit)
    .all()
  )

  return PaginationResponseDTO(
    page=page,
    pages=pages,
    items=items,
    data=result,
    next=None,
    prev=None
  )


# -----------------------------------------------------------------
# GET BY ID    
def get_by_id(db: Session, id: int):
  return (
    db.query(models.News)
    .options(joinedload(models.News.images))
    .filter(models.News.id_news == id)
    .first()
  )


# -----------------------------------------------------------------
# CREATE
def create(db: Session, data: dict):
  new_item = models.News(**data)
  
  db.add(new_item)
  db.commit()
  db.refresh(new_item)

  return new_item


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, id: int, data: dict):
  item = db.query(models.News).filter(models.News.id_news == id).first()

  if not item:
    return None

  for key, value in data.items():
    setattr(item, key, value)
  
  db.commit()
  db.refresh(item)
  return item


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, id: int):
  item = db.query(models.News).filter(models.News.id_news == id).first()
  
  if not item:
    return 0

  db.delete(item)
  db.commit()
  return True