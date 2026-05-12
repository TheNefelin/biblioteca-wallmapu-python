from math import ceil
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session, joinedload

from src.api.book_authors import models as book_authors_model
from src.api.book_subjects import models as book_subjects_model
from src.api.editions import models as edition_models
from src.api.copy import models as copy_model
from src.api.authors import models as authors_models
from src.api.genres import models as genre_models
from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO

from . import models


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(
  db: Session,
  pagination: PaginationRequestDTO
) -> PaginationResponseDTO:
  first_author_subq = (
    db.query(
      book_authors_model.BookAuthor.id_book,
      authors_models.Author.id_author.label("author_id"),
      authors_models.Author.name.label("author_name"),
      func.row_number().over(
        partition_by=book_authors_model.BookAuthor.id_book,
        order_by=book_authors_model.BookAuthor.id_author
      ).label("rn")
    )
    .join(authors_models.Author, book_authors_model.BookAuthor.id_author == authors_models.Author.id_author)
    .subquery()
  )

  edition_count_subq = (
    db.query(
      edition_models.Edition.book_id,
      func.count(edition_models.Edition.id_edition).label("edition_count")
    )
    .group_by(edition_models.Edition.book_id)
    .subquery()
  )

  first_cover_subq = (
    db.query(
      edition_models.Edition.book_id,
      edition_models.Edition.cover_image.label("cover_image"),
      func.row_number().over(
        partition_by=edition_models.Edition.book_id,
        order_by=edition_models.Edition.id_edition
      ).label("rn")
    )
    .subquery()
  )

  copy_count_subq = (
    db.query(
      edition_models.Edition.book_id,
      func.count(copy_model.Copy.id_copy).label("copy_count")
    )
    .join(copy_model.Copy, copy_model.Copy.edition_id == edition_models.Edition.id_edition)
    .group_by(edition_models.Edition.book_id)
    .subquery()
  )

  query = (
    db.query(
      models.Book.id_book,
      models.Book.title,
      first_cover_subq.c.cover_image.label("edition_cover_image"),
      models.Book.created_at,
      models.Book.updated_at,
      models.Book.genre_id,
      genre_models.Genre.name.label("genre_name"),
      func.coalesce(first_author_subq.c.author_id, 0).label("author_id"),
      func.coalesce(first_author_subq.c.author_name, "Sin Autor").label("author_name"),
      func.coalesce(edition_count_subq.c.edition_count, 0).label("edition_count"),
      func.coalesce(copy_count_subq.c.copy_count, 0).label("copy_count"),
    )
    .join(genre_models.Genre, models.Book.genre_id == genre_models.Genre.id_genre)
    .outerjoin(
      first_author_subq,
      and_(
        models.Book.id_book == first_author_subq.c.id_book,
        first_author_subq.c.rn == 1
      )
    )
    .outerjoin(
      edition_count_subq,
      models.Book.id_book == edition_count_subq.c.book_id
    )
    .outerjoin(
      first_cover_subq,
      and_(
        models.Book.id_book == first_cover_subq.c.book_id,
        first_cover_subq.c.rn == 1
      )
    )
    .outerjoin(
      copy_count_subq,
      models.Book.id_book == copy_count_subq.c.book_id
    )
  )

  if pagination.search:
    query = query.filter(
      or_(
        models.Book.title.ilike(f"%{pagination.search}%"),
        models.Book.summary.ilike(f"%{pagination.search}%"),
      )
    )

  total_items = query.count()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (
    query
    .order_by(models.Book.updated_at.desc())
    .offset(offset)
    .limit(pagination.limit)
    .all()
  )

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=result,
    next=None,
    prev=None,
  )


# -----------------------------------------------------------------
# GET BY ID
def get_by_id(db: Session, id: int) -> models.Book | None:
  return (
    db.query(models.Book)
    .filter(models.Book.id_book == id)
    .options(
      joinedload(models.Book.genre),
      joinedload(models.Book.book_authors).joinedload(book_authors_model.BookAuthor.author),
      joinedload(models.Book.book_subjects).joinedload(book_subjects_model.BookSubject.subject),
    )
    .first()
  )


# -----------------------------------------------------------------
# CREATE
def create(db: Session, data: dict) -> models.Book:
  book = models.Book(**data)
  db.add(book)
  db.commit()
  db.refresh(book)
  return book


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, book: models.Book, data: dict) -> models.Book:
  for key, value in data.items():
    setattr(book, key, value)
  db.commit()
  db.refresh(book)
  return book


# -----------------------------------------------------------------
# GET ENTITY BY ID
def get_entity_by_id(db: Session, id: int) -> models.Book | None:
  return db.get(models.Book, id)


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, book: models.Book) -> None:
  db.delete(book)
  db.commit()


# -----------------------------------------------------------------
# HAS AUTHORS
def has_authors(db: Session, book_id: int) -> bool:
  return db.query(book_authors_model.BookAuthor).filter_by(id_book=book_id).first() is not None


# -----------------------------------------------------------------
# HAS SUBJECTS
def has_subjects(db: Session, book_id: int) -> bool:
  return db.query(book_subjects_model.BookSubject).filter_by(id_book=book_id).first() is not None


# -----------------------------------------------------------------
# HAS EDITIONS
def has_editions(db: Session, book_id: int) -> bool:
  return db.query(edition_models.Edition).filter_by(book_id=book_id).first() is not None
