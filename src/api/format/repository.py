import unicodedata
from math import ceil
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import EditionFormat, Format
from src.schemas.dtos import PaginationRequestDTO, PaginationResponseDTO


# -----------------------------------------------------------------#
# GET ALL PAGINATION
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  search_norm = None
  if pagination.search:
    search_norm = unicodedata.normalize('NFKD', pagination.search).encode('ascii', 'ignore').decode('ascii')

  query = select(Format).order_by(Format.name.asc())

  if search_norm:
    query = query.where(func.unaccent(Format.name).ilike(f"%{search_norm}%"))

  total_items = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar_one()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = list((await db.execute(query.offset(offset).limit(pagination.limit))).scalars().all())

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=result,
  )


# -----------------------------------------------------------------#
# GET ALL
async def get_all(db: AsyncSession) -> list[Format]:
  result = await db.execute(select(Format).order_by(Format.name.asc()))
  return list(result.scalars().all())


# -----------------------------------------------------------------#
# GET BY NAME
async def get_by_name(db: AsyncSession, name: str) -> Format | None:
  result = await db.execute(select(Format).where(Format.name.ilike(name)))
  return result.scalar_one_or_none()


# -----------------------------------------------------------------#
# CREATE
async def create(db: AsyncSession, data: dict) -> Format | None:
  item = Format(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


# -----------------------------------------------------------------#
# UPDATE
async def update(db: AsyncSession, id: int, data: dict) -> Format | None:
  result = await db.execute(select(Format).where(Format.id_format == id))
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
    select(EditionFormat).where(EditionFormat.id_format == id)
  )
  if relations_result.scalars().first():
    return False

  result = await db.execute(select(Format).where(Format.id_format == id))
  item = result.scalar_one_or_none()

  if not item:
    return None

  await db.delete(item)
  await db.commit()
  return True
