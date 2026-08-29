from math import ceil
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.schemas.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.models import models


# -----------------------------------------------------------------
# GET ALL Pagination
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  stmt = select(models.News).options(
    selectinload(models.News.images)
  )

  if pagination.search:
    stmt = stmt.where(
      or_(
        models.News.title.ilike(f"%{pagination.search}%"),
        models.News.subtitle.ilike(f"%{pagination.search}%")
      )
    )

  items_result = await db.execute(
    select(func.count()).select_from(stmt.subquery())
  )
  items = items_result.scalar_one()

  pages = ceil(items / pagination.limit) if items > 0 else 0
  page = min(pagination.page, pages) if pages > 0 else 1
  skip = (page - 1) * pagination.limit

  result = (await db.execute(
    stmt
    .order_by(models.News.created_at.desc())
    .offset(skip)
    .limit(pagination.limit)
  )).scalars().all()

  return PaginationResponseDTO(
    page=page,
    pages=pages,
    items=items,
    data=list(result),
    next=None,
    prev=None,
  )


# -----------------------------------------------------------------
# GET BY ID
async def get_by_id(db: AsyncSession, id: int):
  result = await db.execute(
    select(models.News)
    .options(selectinload(models.News.images))
    .where(models.News.id_news == id)
  )
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, data: dict):
  new_item = models.News(**data)
  db.add(new_item)
  await db.commit()
  await db.refresh(new_item)
  return new_item


# -----------------------------------------------------------------
# UPDATE
async def update(db: AsyncSession, id: int, data: dict):
  item = (await db.execute(
    select(models.News).where(models.News.id_news == id)
  )).scalar_one_or_none()

  if not item:
    return None

  for key, value in data.items():
    setattr(item, key, value)

  await db.commit()
  await db.refresh(item)
  return item


# -----------------------------------------------------------------
# DELETE
async def delete(db: AsyncSession, id: int):
  item = (await db.execute(
    select(models.News).where(models.News.id_news == id)
  )).scalar_one_or_none()

  if not item:
    return 0

  await db.delete(item)
  await db.commit()
  return True