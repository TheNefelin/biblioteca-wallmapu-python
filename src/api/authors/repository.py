from math import ceil
from fastapi import Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  try:
    query = db.query(models.Author)

    search_filter = pagination.search if pagination.search else None
    if search_filter:
      query = query.filter(
        models.Author.name.ilike(f"%{search_filter}%")
      )

    total_items = query.count()
    total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
    
    page = min(pagination.page, total_pages) if total_pages > 0 else 1
    offset = (page - 1) * pagination.limit

    result = (
      query
      .order_by(models.Author.name.asc())
      .offset(offset)
      .limit(pagination.limit)
      .all()
    )

    next_url = f"/api/author/pagination?page={page + 1}&limit={pagination.limit}" if page < total_pages else None
    prev_url = f"/api/author/pagination?page={page - 1}&limit={pagination.limit}" if page > 1 else None

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
def get_all(db: Session) -> list[models.Author]:
  return (
    db.query(models.Author)
    .order_by(models.Author.name.asc())
    .all()
  )


# -----------------------------------------------------------------
# CREATE
def create(db: Session, data: dict) -> models.Author | None:
  try:
    author = models.Author(**data)
    db.add(author)
    db.commit()
    db.refresh(author)

    return author
  except SQLAlchemyError as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, id: int, data: dict) -> models.Author | None:
  try:
    author = (
      db.query(models.Author)
      .filter(models.Author.id_author == id)
      .first()
    )

    if not author:
      return None
    
    for key, value in data.items():
      setattr(author, key, value)
    
    db.commit()
    db.refresh(author)

    return author
  except SQLAlchemyError as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, id: int) -> bool | None:
  try:
    # Lazy import para evitar circular import
    from src.api.book_authors import models as book_author_models

    # Verificar si el autor tiene relaciones con libros
    relations = db.query(book_author_models.BookAuthor).filter(
      book_author_models.BookAuthor.id_author == id
    ).first()

    if relations:
      return False  # No se puede eliminar, tiene libros asociados

    author = (
      db.query(models.Author)
      .filter(models.Author.id_author == id)
      .first()
    )

    if not author:
      return None

    db.delete(author)
    db.commit()

    return True
  except SQLAlchemyError as e:
    db.rollback()
    raise e
