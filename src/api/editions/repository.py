from math import ceil
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session, joinedload

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from .dtos import EditionFilterDTO
from src.api.books import models as book_models
from src.api.authors import models as authors_models
from src.api.book_authors import models as book_authors_models
from src.api.copy import models as copy_models
from src.api.editorials import models as editorial_models
from src.api.genres import models as genre_models
from src.api.edition_format import models as edition_format_models
from src.api.book_subjects import models as book_subjects_models
from . import models


def _build_first_author_subq(db: Session):
  return (
    db.query(
      book_authors_models.BookAuthor.id_book,
      authors_models.Author.id_author.label("author_id"),
      authors_models.Author.name.label("author_name"),
      func.row_number().over(
        partition_by=book_authors_models.BookAuthor.id_book,
        order_by=book_authors_models.BookAuthor.id_author
      ).label("rn")
    )
    .join(authors_models.Author, book_authors_models.BookAuthor.id_author == authors_models.Author.id_author)
    .subquery()
  )


def _build_copy_count_subq(db: Session):
  return (
    db.query(
      copy_models.Copy.edition_id,
      func.count(copy_models.Copy.id_copy).label("copy_count")
    )
    .group_by(copy_models.Copy.edition_id)
    .subquery()
  )


# -----------------------------------------------------------------
# GET ALL PAGINATION REAL (flat DTO, column-based query)
def get_all_pagination(
    db: Session,
    pagination: PaginationRequestDTO[EditionFilterDTO]
) -> PaginationResponseDTO:
  first_author_subq = _build_first_author_subq(db)
  copy_count_subq = _build_copy_count_subq(db)

  query = (
    db.query(
      models.Edition.id_edition,
      models.Edition.edition,
      models.Edition.isbn,
      models.Edition.publication_year,
      models.Edition.pages,
      models.Edition.cover_image,
      models.Edition.created_at,
      models.Edition.updated_at,
      models.Edition.editorial_id,
      editorial_models.Editorial.name.label("editorial_name"),
      models.Edition.book_id,
      book_models.Book.title.label("book_title"),
      book_models.Book.genre_id.label("genre_id"),
      genre_models.Genre.name.label("genre_name"),
      func.coalesce(first_author_subq.c.author_id, 0).label("author_id"),
      func.coalesce(first_author_subq.c.author_name, "Sin Autor").label("author_name"),
      func.coalesce(copy_count_subq.c.copy_count, 0).label("copy_count"),
    )
    .join(book_models.Book, models.Edition.book_id == book_models.Book.id_book)
    .join(editorial_models.Editorial, models.Edition.editorial_id == editorial_models.Editorial.id_editorial)
    .join(genre_models.Genre, book_models.Book.genre_id == genre_models.Genre.id_genre)
    .outerjoin(
      first_author_subq,
      and_(
        book_models.Book.id_book == first_author_subq.c.id_book,
        first_author_subq.c.rn == 1
      )
    )
    .outerjoin(
      copy_count_subq,
      models.Edition.id_edition == copy_count_subq.c.edition_id
    )
  )

  if pagination.search:
    query = query.filter(
      or_(
        func.unaccent(models.Edition.isbn).ilike(f"%{pagination.search}%"),
        func.unaccent(book_models.Book.title).ilike(f"%{pagination.search}%"),
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
      query = query.filter(models.Edition.editorial_id == pagination.filter.id_editorial)
    if pagination.filter.id_genre:
      query = query.filter(book_models.Book.genre_id == pagination.filter.id_genre)
    if pagination.filter.id_format:
      query = query.join(
        edition_format_models.EditionFormat,
        models.Edition.id_edition == edition_format_models.EditionFormat.id_edition
      ).filter(
        edition_format_models.EditionFormat.id_format == pagination.filter.id_format
      )
    if pagination.filter.id_subject:
      query = query.join(book_models.Book.book_subjects).filter(
        book_subjects_models.BookSubject.id_subject == pagination.filter.id_subject
      )

  query = query.distinct()
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

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=result,
    next=None,
    prev=None,
  )


# -----------------------------------------------------------------
# GET BY BOOK ID DETAIL (flat DTO, column-based)
def get_by_book_id_detail(db: Session, book_id: int) -> list:
  first_author_subq = _build_first_author_subq(db)
  copy_count_subq = _build_copy_count_subq(db)

  return (
    db.query(
      models.Edition.id_edition,
      models.Edition.edition,
      models.Edition.isbn,
      models.Edition.publication_year,
      models.Edition.pages,
      models.Edition.cover_image,
      models.Edition.created_at,
      models.Edition.updated_at,
      models.Edition.editorial_id,
      editorial_models.Editorial.name.label("editorial_name"),
      models.Edition.book_id,
      book_models.Book.title.label("book_title"),
      book_models.Book.genre_id.label("genre_id"),
      genre_models.Genre.name.label("genre_name"),
      func.coalesce(first_author_subq.c.author_id, 0).label("author_id"),
      func.coalesce(first_author_subq.c.author_name, "Sin Autor").label("author_name"),
      func.coalesce(copy_count_subq.c.copy_count, 0).label("copy_count"),
    )
    .join(book_models.Book, models.Edition.book_id == book_models.Book.id_book)
    .join(editorial_models.Editorial, models.Edition.editorial_id == editorial_models.Editorial.id_editorial)
    .join(genre_models.Genre, book_models.Book.genre_id == genre_models.Genre.id_genre)
    .outerjoin(
      first_author_subq,
      and_(
        book_models.Book.id_book == first_author_subq.c.id_book,
        first_author_subq.c.rn == 1
      )
    )
    .outerjoin(
      copy_count_subq,
      models.Edition.id_edition == copy_count_subq.c.edition_id
    )
    .filter(models.Edition.book_id == book_id)
    .order_by(models.Edition.edition.asc())
    .all()
  )


# -----------------------------------------------------------------
# GET BY BOOK ID (básico, sin joins)
def get_by_book_id(db: Session, book_id: int) -> list[models.Edition]:
  return (
    db.query(models.Edition)
    .filter(models.Edition.book_id == book_id)
    .options(
      joinedload(models.Edition.edition_formats).joinedload(edition_format_models.EditionFormat.format_rel),
    )
    .order_by(models.Edition.edition.asc())
    .all()
  )


# -----------------------------------------------------------------
# GET BY ID (con joins para formatos)
def get_by_id(db: Session, id: int) -> models.Edition | None:
  return (
    db.query(models.Edition)
    .filter(models.Edition.id_edition == id)
    .options(
      joinedload(models.Edition.edition_formats).joinedload(edition_format_models.EditionFormat.format_rel),
    )
    .first()
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
  url = edition.cover_image
  db.delete(edition)
  db.commit()
  return url


# -----------------------------------------------------------------
# HAS COPIES
def has_copies(db: Session, edition_id: int) -> bool:
  return db.query(copy_models.Copy).filter(copy_models.Copy.edition_id == edition_id).first() is not None
