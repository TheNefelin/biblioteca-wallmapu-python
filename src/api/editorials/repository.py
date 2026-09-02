import unicodedata
from datetime import datetime
from math import ceil
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Edition, Editorial
from src.schemas.dtos import PaginationRequestDTO, PaginationResponseDTO


# -----------------------------------------------------------------
# GET ALL PAGINATION
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  search_norm = None
  if pagination.search and pagination.search.strip():
    search_norm = unicodedata.normalize('NFKD', pagination.search).encode('ascii', 'ignore').decode('ascii')

  query = select(Editorial).order_by(Editorial.name.asc())

  if search_norm:
    query = query.where(func.unaccent(Editorial.name).ilike(f"%{search_norm}%"))

  total_items = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar_one()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  items = list((await db.execute(query.offset(offset).limit(pagination.limit))).scalars().all())

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=items,
  )


# -----------------------------------------------------------------
# GET ALL
async def get_all(db: AsyncSession) -> list[Editorial]:
  result = await db.execute(select(Editorial).order_by(Editorial.name.asc()))
  return list(result.scalars().all())


# -----------------------------------------------------------------
# GET BY ID
async def get_by_id(db: AsyncSession, id: int) -> Editorial | None:
  result = await db.execute(select(Editorial).where(Editorial.id_editorial == id))
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# EXISTS BY NAME
async def exists_by_name(db: AsyncSession, name: str, exclude_id: int | None = None) -> bool:
  query = select(Editorial).where(Editorial.name.ilike(name))
  if exclude_id:
    query = query.where(Editorial.id_editorial != exclude_id)
  result = await db.execute(query)
  return result.scalar_one_or_none() is not None


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, data: dict) -> Editorial:
  entity = Editorial(**data)
  db.add(entity)
  await db.commit()
  await db.refresh(entity)
  return entity


# -----------------------------------------------------------------
# UPDATE
async def update(db: AsyncSession, entity: Editorial, update_data: dict) -> Editorial:
  for key, value in update_data.items():
    setattr(entity, key, value)
  entity.updated_at = datetime.now()
  await db.commit()
  await db.refresh(entity)
  return entity


# -----------------------------------------------------------------
# DELETE
async def delete(db: AsyncSession, id: int) -> bool | None:
  relations_result = await db.execute(
    select(Edition).where(Edition.editorial_id == id)
  )
  if relations_result.scalars().first():
    return False

  result = await db.execute(select(Editorial).where(Editorial.id_editorial == id))
  item = result.scalar_one_or_none()

  if not item:
    return None

  await db.delete(item)
  await db.commit()
  return True


# -----------------------------------------------------------------
# EXISTS BY ID
async def exists_by_id(db: AsyncSession, id: int) -> bool:
  result = await db.execute(select(Editorial).where(Editorial.id_editorial == id))
  return result.scalar_one_or_none() is not None
