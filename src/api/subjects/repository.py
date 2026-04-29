from math import ceil
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  try:
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

    next_url = f"/api/subject/pagination?page={page + 1}&limit={pagination.limit}" if page < total_pages else None
    prev_url = f"/api/subject/pagination?page={page - 1}&limit={pagination.limit}" if page > 1 else None

    return PaginationResponseDTO(
      page=page,
      pages=total_pages,
      items=total_items,
      data=result,
      next=next_url,
      prev=prev_url
    )
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Subject]:
  try:
    return (
      db.query(models.Subject)
      .order_by(models.Subject.name.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# CREATE
def create(db: Session, data: dict) -> models.Subject | None:
  try:
    item = models.Subject(**data)
    db.add(item)
    db.commit()
    db.refresh(item)

    return item
  except SQLAlchemyError as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, id: int, data: dict) -> models.Subject | None:
  try:
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
  except SQLAlchemyError as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, id: int) -> bool | None:
  try:
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
  except SQLAlchemyError as e:
    db.rollback()
    raise e

