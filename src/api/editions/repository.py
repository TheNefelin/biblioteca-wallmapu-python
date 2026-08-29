import unicodedata
from math import ceil
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.schemas.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.schemas.dtos import EditionFilterDTO
from src.models import models


def _build_first_author_subq():
  return (
    select(
      models.BookAuthor.id_book,
      models.Author.id_author.label("author_id"),
      models.Author.name.label("author_name"),
      func.row_number().over(
        partition_by=models.BookAuthor.id_book,
        order_by=models.BookAuthor.id_author
      ).label("rn")
    )
    .join(models.Author, models.BookAuthor.id_author == models.Author.id_author)
    .subquery()
  )


def _build_copy_count_subq():
  return (
    select(
      models.Copy.edition_id,
      func.count(models.Copy.id_copy).label("copy_count")
    )
    .group_by(models.Copy.edition_id)
    .subquery()
  )


# -----------------------------------------------------------------
# GET ALL PAGINATION REAL (flat DTO, column-based query)
async def get_all_pagination(
    db: AsyncSession,
    pagination: PaginationRequestDTO[EditionFilterDTO]
) -> PaginationResponseDTO:
  first_author_subq = _build_first_author_subq()
  copy_count_subq = _build_copy_count_subq()

  query = (
    select(
      models.Edition.id_edition,
      models.Edition.edition,
      models.Edition.isbn,
      models.Edition.publication_year,
      models.Edition.pages,
      models.Edition.cover_image,
      models.Edition.created_at,
      models.Edition.updated_at,
      models.Edition.editorial_id,
      models.Editorial.name.label("editorial_name"),
      models.Edition.book_id,
      models.Book.title.label("book_title"),
      models.Book.genre_id.label("genre_id"),
      models.Genre.name.label("genre_name"),
      func.coalesce(first_author_subq.c.author_id, 0).label("author_id"),
      func.coalesce(first_author_subq.c.author_name, "Sin Autor").label("author_name"),
      func.coalesce(copy_count_subq.c.copy_count, 0).label("copy_count"),
    )
    .join(models.Book, models.Edition.book_id == models.Book.id_book)
    .join(models.Editorial, models.Edition.editorial_id == models.Editorial.id_editorial)
    .join(models.Genre, models.Book.genre_id == models.Genre.id_genre)
    .outerjoin(
      first_author_subq,
      and_(
        models.Book.id_book == first_author_subq.c.id_book,
        first_author_subq.c.rn == 1
      )
    )
    .outerjoin(
      copy_count_subq,
      models.Edition.id_edition == copy_count_subq.c.edition_id
    )
  )

  if pagination.search:
    search_norm = unicodedata.normalize('NFKD', pagination.search).encode('ascii', 'ignore').decode('ascii')
    query = query.where(
      or_(
        func.unaccent(models.Edition.isbn).ilike(f"%{search_norm}%"),
        func.unaccent(models.Book.title).ilike(f"%{search_norm}%"),
      )
    )

  if pagination.filter:
    if pagination.filter.id_author:
      query = (
        query.join(models.Book.book_authors)
        .join(models.BookAuthor.author)
        .where(models.Author.id_author == pagination.filter.id_author)
      )
    if pagination.filter.id_editorial:
      query = query.where(models.Edition.editorial_id == pagination.filter.id_editorial)
    if pagination.filter.id_genre:
      query = query.where(models.Book.genre_id == pagination.filter.id_genre)
    if pagination.filter.id_format:
      query = query.join(
        models.EditionFormat,
        models.Edition.id_edition == models.EditionFormat.id_edition
      ).where(
        models.EditionFormat.id_format == pagination.filter.id_format
      )
    if pagination.filter.id_subject:
      query = query.join(models.Book.book_subjects).where(
        models.BookSubject.id_subject == pagination.filter.id_subject
      )

  query = query.distinct()

  total_items_result = await db.execute(select(func.count()).select_from(query.subquery()))
  total_items = total_items_result.scalar_one()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (await db.execute(
    query
    .order_by(models.Edition.updated_at.desc())
    .offset(offset)
    .limit(pagination.limit)
  )).all()

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=list(result),
    next=None,
    prev=None,
  )


# -----------------------------------------------------------------
# GET BY BOOK ID DETAIL (flat DTO, column-based)
async def get_by_book_id_detail(db: AsyncSession, book_id: int) -> list:
  first_author_subq = _build_first_author_subq()
  copy_count_subq = _build_copy_count_subq()

  result = await db.execute(
    select(
      models.Edition.id_edition,
      models.Edition.edition,
      models.Edition.isbn,
      models.Edition.publication_year,
      models.Edition.pages,
      models.Edition.cover_image,
      models.Edition.created_at,
      models.Edition.updated_at,
      models.Edition.editorial_id,
      models.Editorial.name.label("editorial_name"),
      models.Edition.book_id,
      models.Book.title.label("book_title"),
      models.Book.genre_id.label("genre_id"),
      models.Genre.name.label("genre_name"),
      func.coalesce(first_author_subq.c.author_id, 0).label("author_id"),
      func.coalesce(first_author_subq.c.author_name, "Sin Autor").label("author_name"),
      func.coalesce(copy_count_subq.c.copy_count, 0).label("copy_count"),
    )
    .join(models.Book, models.Edition.book_id == models.Book.id_book)
    .join(models.Editorial, models.Edition.editorial_id == models.Editorial.id_editorial)
    .join(models.Genre, models.Book.genre_id == models.Genre.id_genre)
    .outerjoin(
      first_author_subq,
      and_(
        models.Book.id_book == first_author_subq.c.id_book,
        first_author_subq.c.rn == 1
      )
    )
    .outerjoin(
      copy_count_subq,
      models.Edition.id_edition == copy_count_subq.c.edition_id
    )
    .where(models.Edition.book_id == book_id)
    .order_by(models.Edition.edition.asc())
  )
  return result.all()


# -----------------------------------------------------------------
# GET BY BOOK ID (bÃ¡sico, sin joins)
async def get_by_book_id(db: AsyncSession, book_id: int) -> list[models.Edition]:
  result = await db.execute(
    select(models.Edition)
    .where(models.Edition.book_id == book_id)
    .options(
      selectinload(models.Edition.edition_formats).selectinload(models.EditionFormat.format_rel),
    )
    .order_by(models.Edition.edition.asc())
  )
  return list(result.scalars().all())


# -----------------------------------------------------------------
# GET BY ID (con joins para formatos)
async def get_by_id(db: AsyncSession, id: int) -> models.Edition | None:
  result = await db.execute(
    select(models.Edition)
    .where(models.Edition.id_edition == id)
    .options(
      selectinload(models.Edition.edition_formats).selectinload(models.EditionFormat.format_rel),
    )
  )
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# GET ENTITY BY ID (sin joins)
async def get_entity_by_id(db: AsyncSession, id: int) -> models.Edition | None:
  return await db.get(models.Edition, id)


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, data: dict) -> models.Edition:
  item = models.Edition(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


# -----------------------------------------------------------------
# UPDATE
async def update(db: AsyncSession, item: models.Edition, data: dict) -> models.Edition:
  for key, value in data.items():
    setattr(item, key, value)
  await db.commit()
  await db.refresh(item)
  return item


# -----------------------------------------------------------------
# DELETE
async def delete(db: AsyncSession, edition: models.Edition) -> str | None:
  url = edition.cover_image
  await db.delete(edition)
  await db.commit()
  return url


# -----------------------------------------------------------------
# HAS COPIES
async def has_copies(db: AsyncSession, edition_id: int) -> bool:
  result = await db.execute(
    select(models.Copy).where(models.Copy.edition_id == edition_id)
  )
  return result.first() is not None