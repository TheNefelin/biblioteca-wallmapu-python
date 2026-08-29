from math import ceil
from sqlalchemy import func, or_, select, update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import models
from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO


# -----------------------------------------------------------------
# GET ALL PAGINATED (Admin)
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  stmt = select(models.Notification).options(
    selectinload(models.Notification.user)
  )

  is_read_filter = pagination.filter.is_read if pagination.filter else True
  if not is_read_filter:
    stmt = stmt.where(models.Notification.is_read == False)

  search_filter = pagination.search if pagination.search else None
  if search_filter:
    stmt = stmt.where(
      or_(
        models.Notification.title.ilike(f"%{search_filter}%"),
        models.Notification.message.ilike(f"%{search_filter}%")
      )
    )

  total_items_result = await db.execute(select(func.count()).select_from(stmt.subquery()))
  total_items = total_items_result.scalar_one()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0

  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (await db.execute(
    stmt
    .order_by(models.Notification.created_at.desc())
    .offset(offset)
    .limit(pagination.limit)
  )).scalars().all()

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=list(result),
    next=None,
    prev=None
  )


# -----------------------------------------------------------------
# GET BY USER PAGINATED
async def get_by_user_paginated(db: AsyncSession, user_id: str, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  stmt = select(models.Notification).options(
    selectinload(models.Notification.user)
  ).where(models.Notification.user_id == user_id)

  is_read_filter = pagination.filter.is_read if pagination.filter else True
  if not is_read_filter:
    stmt = stmt.where(models.Notification.is_read == False)

  search_filter = pagination.search if pagination.search else None
  if search_filter:
    stmt = stmt.where(
      or_(
        models.Notification.title.ilike(f"%{search_filter}%"),
        models.Notification.message.ilike(f"%{search_filter}%")
      )
    )

  total_items_result = await db.execute(select(func.count()).select_from(stmt.subquery()))
  total_items = total_items_result.scalar_one()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0

  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (await db.execute(
    stmt
    .order_by(models.Notification.created_at.desc())
    .offset(offset)
    .limit(pagination.limit)
  )).scalars().all()

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=list(result),
    next=None,
    prev=None
  )


# -----------------------------------------------------------------
# GET BY ID
async def get_by_id(db: AsyncSession, id: int):
  result = await db.execute(
    select(models.Notification)
    .options(selectinload(models.Notification.user))
    .where(models.Notification.id_notification == id)
  )
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# COUNT UNREAD BY USER (For badge)
async def count_unread_by_user_id(db: AsyncSession, user_id: str) -> int:
  result = await db.execute(
    select(func.count())
    .select_from(models.Notification)
    .where(
      models.Notification.user_id == user_id,
      models.Notification.is_read == False
    )
  )
  return result.scalar_one()


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, data: dict) -> models.Notification | None:
  item = models.Notification(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


# -----------------------------------------------------------------
# MARK AS READ
async def mark_as_read(db: AsyncSession, id: int):
  notification = (await db.execute(
    select(models.Notification).where(models.Notification.id_notification == id)
  )).scalar_one_or_none()
  if notification:
    notification.is_read = True
    await db.commit()
    await db.refresh(notification)
  return notification


# -----------------------------------------------------------------
# MARK ALL AS READ
async def mark_all_as_read(db: AsyncSession, user_id: str):
  result = await db.execute(
    sa_update(models.Notification)
    .where(
      models.Notification.user_id == user_id,
      models.Notification.is_read == False
    )
    .values(is_read=True)
  )
  await db.commit()
  return result.rowcount