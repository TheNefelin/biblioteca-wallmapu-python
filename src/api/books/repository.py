from math import ceil
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import models
from src.schemas.dtos import PaginationRequestDTO, PaginationResponseDTO


# -----------------------------------------------------------------
# GET ALL PAGINATION
async def get_all_pagination(
  db: AsyncSession,
  pagination: PaginationRequestDTO
) -> PaginationResponseDTO:
  first_author_subq = (
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

  edition_count_subq = (
    select(
      models.Edition.book_id,
      func.count(models.Edition.id_edition).label("edition_count")
    )
    .group_by(models.Edition.book_id)
    .subquery()
  )

  first_cover_subq = (
    select(
      models.Edition.book_id,
      models.Edition.cover_image.label("cover_image"),
      func.row_number().over(
        partition_by=models.Edition.book_id,
        order_by=models.Edition.id_edition
      ).label("rn")
    )
    .subquery()
  )

  copy_count_subq = (
    select(
      models.Edition.book_id,
      func.count(models.Copy.id_copy).label("copy_count")
    )
    .join(models.Copy, models.Copy.edition_id == models.Edition.id_edition)
    .group_by(models.Edition.book_id)
    .subquery()
  )

  query = (
    select(
      models.Book.id_book,
      models.Book.title,
      first_cover_subq.c.cover_image.label("edition_cover_image"),
      models.Book.created_at,
      models.Book.updated_at,
      models.Book.genre_id,
      models.Genre.name.label("genre_name"),
      func.coalesce(first_author_subq.c.author_id, 0).label("author_id"),
      func.coalesce(first_author_subq.c.author_name, "Sin Autor").label("author_name"),
      func.coalesce(edition_count_subq.c.edition_count, 0).label("edition_count"),
      func.coalesce(copy_count_subq.c.copy_count, 0).label("copy_count"),
    )
    .join(models.Genre, models.Book.genre_id == models.Genre.id_genre)
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

  total_items_result = await db.execute(select(func.count()).select_from(query.subquery()))
  total_items = total_items_result.scalar_one()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (await db.execute(
    query
    .order_by(models.Book.updated_at.desc(), models.Book.id_book.desc())
    .offset(offset)
    .limit(pagination.limit)
  )).scalars().all()

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=list(result),
    next=None,
    prev=None,
  )


# -----------------------------------------------------------------
# GET BY ID
async def get_by_id(db: AsyncSession, id: int) -> models.Book | None:
  result = await db.execute(
    select(models.Book)
    .filter(models.Book.id_book == id)
    .options(
      selectinload(models.Book.genre),
      selectinload(models.Book.book_authors).selectinload(models.BookAuthor.author),
      selectinload(models.Book.book_subjects).selectinload(models.BookSubject.subject),
    )
  )
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, data: dict) -> models.Book:
  book = models.Book(**data)
  db.add(book)
  await db.commit()
  await db.refresh(book)
  return book


# -----------------------------------------------------------------
# UPDATE
async def update(db: AsyncSession, book: models.Book, data: dict) -> models.Book:
  for key, value in data.items():
    setattr(book, key, value)
  await db.commit()
  await db.refresh(book)
  return book


# -----------------------------------------------------------------
# GET ENTITY BY ID
async def get_entity_by_id(db: AsyncSession, id: int) -> models.Book | None:
  return await db.get(models.Book, id)


# -----------------------------------------------------------------
# DELETE
async def delete(db: AsyncSession, book: models.Book) -> None:
  await db.delete(book)
  await db.commit()


# -----------------------------------------------------------------
# HAS AUTHORS
async def has_authors(db: AsyncSession, book_id: int) -> bool:
  result = await db.execute(
    select(models.BookAuthor).filter(models.BookAuthor.id_book == book_id)
  )
  return result.first() is not None


# -----------------------------------------------------------------
# HAS SUBJECTS
async def has_subjects(db: AsyncSession, book_id: int) -> bool:
  result = await db.execute(
    select(models.BookSubject).filter(models.BookSubject.id_book == book_id)
  )
  return result.first() is not None


# -----------------------------------------------------------------
# HAS EDITIONS
async def has_editions(db: AsyncSession, book_id: int) -> bool:
  result = await db.execute(
    select(models.Edition).filter(models.Edition.book_id == book_id)
  )
  return result.first() is not None