import unicodedata
from math import ceil
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Book, Genre
from src.schemas.dtos import PaginationRequest, PaginationResponse


# -----------------------------------------------------------------#
# GET ALL PAGINATION
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequest) -> PaginationResponse:
  search_norm = None
  if pagination.search:
    search_norm = unicodedata.normalize('NFKD', pagination.search).encode('ascii', 'ignore').decode('ascii')

  query = select(Genre).order_by(Genre.name.asc())

  if search_norm:
    query = query.where(func.unaccent(Genre.name).ilike(f"%{search_norm}%"))

  total_items = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar_one()

  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = list((await db.execute(query.offset(offset).limit(pagination.limit))).scalars().all())

  return PaginationResponse(
    page=page,
    pages=total_pages,
    items=total_items,
    data=result,
  )


# -----------------------------------------------------------------#
# GET ALL
async def get_all(db: AsyncSession) -> list[Genre]:
  result = await db.execute(select(Genre).order_by(Genre.name.asc()))
  return list(result.scalars().all())


# -----------------------------------------------------------------#
# GET BY NAME
async def get_by_name(db: AsyncSession, name: str) -> Genre | None:
  result = await db.execute(select(Genre).where(Genre.name.ilike(name)))
  return result.scalar_one_or_none()


# -----------------------------------------------------------------#
# CREATE
async def create(db: AsyncSession, data: dict) -> Genre | None:
  item = Genre(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


# -----------------------------------------------------------------#
# UPDATE
async def update(db: AsyncSession, id: int, data: dict) -> Genre | None:
  result = await db.execute(select(Genre).where(Genre.id_genre == id))
  item = result.scalar_one_or_none()

  if not item:
    return None

  for key, value in data.items():
    setattr(item, key, value)

  await db.commit()
  await db.refresh(item)
  return item


# -----------------------------------------------------------------#
# DELETE
async def delete(db: AsyncSession, id: int) -> bool | None:
  relations_result = await db.execute(
    select(Book).where(Book.genre_id == id)
  )
  if relations_result.scalars().first():
    return False

  result = await db.execute(select(Genre).where(Genre.id_genre == id))
  item = result.scalar_one_or_none()

  if not item:
    return None

  await db.delete(item)
  await db.commit()
  return True
