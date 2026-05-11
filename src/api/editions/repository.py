from math import ceil
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload, selectinload

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO, BookFilterDTO
from src.api.books import models as book_models
from src.api.authors import models as authors_models
from src.api.book_authors import models as book_authors_models
from src.api.copy import models as copy_models
from . import models


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO[BookFilterDTO]) -> PaginationResponseDTO:
  query = (
    db.query(models.Edition)
    .join(models.Edition.book)
    .options(
      joinedload(models.Edition.editorial),
      joinedload(models.Edition.book),
      selectinload(models.Edition.copies),
    )
  )

  if pagination.search:
    query = query.filter(
      or_(
        models.Edition.isbn.ilike(f"%{pagination.search}%"),
        book_models.Book.title.ilike(f"%{pagination.search}%"),
        book_models.Book.summary.ilike(f"%{pagination.search}%"),
      )
    )

  if pagination.filter:
    if pagination.filter.id_author:
      query = (
        query.join(book_models.Book.book_authors)
          .join(book_authors_models.BookAuthor.author)
          .filter(authors_models.Author.id_author == pagination.filter.id_author)
      )

    if pagination.filter.id_editorial:
      query = query.filter(
        models.Edition.editorial_id == pagination.filter.id_editorial
      )

    if pagination.filter.id_genre:
      query = query.filter(
        book_models.Book.genre_id == pagination.filter.id_genre
      )

  total_items = query.count()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (
    query
    .order_by(models.Edition.updated_at.desc())
    .offset(offset)
    .limit(pagination.limit)
    .all()
  )

  next_url = f"/api/edition/pagination?page={page + 1}&limit={pagination.limit}" if page < total_pages else None
  prev_url = f"/api/edition/pagination?page={page - 1}&limit={pagination.limit}" if page > 1 else None

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=result,
    next=next_url,
    prev=prev_url,
  )


# -----------------------------------------------------------------
# GET ALL (para selects)
def get_all(db: Session) -> list[models.Edition]:
  return (
    db.query(models.Edition)
    .options(
      joinedload(models.Edition.editorial),
      joinedload(models.Edition.book),
      joinedload(models.Edition.copies),
    )
    .order_by(models.Edition.edition.asc())
    .all()
  )


# -----------------------------------------------------------------
# GET DETAIL BY ID
def get_detail_by_id(db: Session, id: int) -> models.Edition | None:
  return (
    db.query(models.Edition)
    .options(
      joinedload(models.Edition.editorial),
      joinedload(models.Edition.book),
      joinedload(models.Edition.copies),
    )
    .filter(models.Edition.id_edition == id)
    .first()
  )


# -----------------------------------------------------------------
# GET BY BOOK ID
def get_by_book_id(db: Session, book_id: int) -> list[models.Edition]:
  return (
    db.query(models.Edition)
    .filter(models.Edition.book_id == book_id)
    .order_by(models.Edition.edition.asc())
    .all()
  )


# -----------------------------------------------------------------
# GET ENTITY BY ID (sin joins)
def get_entity_by_id(db: Session, id: int) -> models.Edition | None:
  return db.get(models.Edition, id)


# -----------------------------------------------------------------
# CREATE
def create(db: Session, data: dict) -> models.Edition:
  item = models.Edition(**data)
  db.add(item)
  db.commit()
  db.refresh(item)
  return item


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, item: models.Edition, data: dict) -> models.Edition:
  for key, value in data.items():
    setattr(item, key, value)
  db.commit()
  db.refresh(item)
  return item


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, edition: models.Edition) -> str | None:
  has_copies = (
    db.query(copy_models.Copy)
    .filter(copy_models.Copy.edition_id == edition.id_edition)
    .first()
  )
  if has_copies:
    raise ValueError(f"La edición ({edition.edition}) tiene copias asociadas")

  url = edition.cover_image
  db.delete(edition)
  db.commit()
  return url
