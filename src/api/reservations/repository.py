from uuid import UUID
from math import ceil
from datetime import datetime
from sqlalchemy import and_, func, select, update as sa_update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import models
from src.schemas.dtos import PaginationRequest, PaginationResponse


def _reservation_detail_options():
  return (
    selectinload(models.Reservation.user),
    selectinload(models.Reservation.copy)
      .selectinload(models.Copy.edition)
      .selectinload(models.Edition.book),
    selectinload(models.Reservation.status),
  )


# -----------------------------------------------------------------
# GET ALL PAGINATION
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequest) -> PaginationResponse:
  stmt = select(models.Reservation).options(*_reservation_detail_options())

  status_filter = pagination.filter.id_status if pagination.filter else None
  if status_filter and status_filter > 0:
    stmt = stmt.where(models.Reservation.reservation_status_id == status_filter)

  total_items_result = await db.execute(select(func.count()).select_from(stmt.subquery()))
  total_items = total_items_result.scalar_one()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0

  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (await db.execute(
    stmt
    .order_by(models.Reservation.reservation_date.desc())
    .offset(offset)
    .limit(pagination.limit)
  )).scalars().all()

  return PaginationResponse(
    page=page,
    pages=total_pages,
    items=total_items,
    data=list(result),
    next=None,
    prev=None
  )


# -----------------------------------------------------------------
# GET USER PAGINATION
async def get_all_pagination_by_user(db: AsyncSession, user_id: UUID, pagination: PaginationRequest) -> PaginationResponse:
  stmt = select(models.Reservation).options(*_reservation_detail_options()).where(models.Reservation.user_id == user_id)

  status_filter = pagination.filter.id_status if pagination.filter else None
  if status_filter and status_filter > 0:
    stmt = stmt.where(models.Reservation.reservation_status_id == status_filter)

  total_items_result = await db.execute(select(func.count()).select_from(stmt.subquery()))
  total_items = total_items_result.scalar_one()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0

  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (await db.execute(
    stmt
    .order_by(models.Reservation.reservation_date.desc())
    .offset(offset)
    .limit(pagination.limit)
  )).scalars().all()

  return PaginationResponse(
    page=page,
    pages=total_pages,
    items=total_items,
    data=list(result),
    next=None,
    prev=None
  )


# -----------------------------------------------------------------
# GET BY ID
async def get_by_id(db: AsyncSession, id: int) -> models.Reservation:
  result = await db.execute(
    select(models.Reservation)
    .options(*_reservation_detail_options())
    .where(models.Reservation.id_reservation == id)
  )
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, data: dict) -> models.Reservation:
  item = models.Reservation(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


# -----------------------------------------------------------------
# UPDATE RESERVATION STATUS
async def update_status(db: AsyncSession, id: int, status_id: int) -> models.Reservation:
  reservation = (await db.execute(
    select(models.Reservation).where(models.Reservation.id_reservation == id)
  )).scalar_one_or_none()

  if reservation:
    reservation.reservation_status_id = status_id
    await db.commit()
    await db.refresh(reservation)

  return reservation


# -----------------------------------------------------------------
# UPDATE - BULK UPDATE STATUS BY CONDITION
async def bulk_update_status_by_expired(db: AsyncSession, old_status_id: int, new_status_id: int) -> int:
  result = await db.execute(
    sa_update(models.Reservation)
    .where(
      and_(
        models.Reservation.reservation_status_id == old_status_id,
        models.Reservation.expiration_date < datetime.now()
      )
    )
    .values(reservation_status_id=new_status_id)
  )
  await db.commit()
  return result.rowcount


# -----------------------------------------------------------------
# GET ACTIVE RESERVATIONS BY BOOK ID
async def get_active_by_book_id(db: AsyncSession, book_id: int) -> list[models.Reservation]:
  result = await db.execute(
    select(models.Reservation)
    .join(models.Copy, models.Reservation.copy_id == models.Copy.id_copy)
    .join(models.Edition, models.Copy.edition_id == models.Edition.id_edition)
    .options(
      selectinload(models.Reservation.user),
      selectinload(models.Reservation.copy),
      selectinload(models.Reservation.status)
    )
    .where(
      and_(
        models.Edition.book_id == book_id,
        models.Reservation.reservation_status_id == 1
      )
    )
    .order_by(models.Reservation.reservation_date.asc())
  )
  return list(result.scalars().all())


# -----------------------------------------------------------------
# GET ACTIVE RESERVATIONS BY USER (returns tuples: id_reservation, id_copy, book_id)
async def get_active_by_user(db: AsyncSession, user_id: UUID) -> list[tuple]:
  """Retorna lista de (id_reservation, id_copy, book_id) activas del usuario"""
  result = await db.execute(
    select(
      models.Reservation.id_reservation,
      models.Reservation.copy_id,
      models.Edition.book_id
    )
    .join(models.Copy, models.Reservation.copy_id == models.Copy.id_copy)
    .join(models.Edition, models.Copy.edition_id == models.Edition.id_edition)
    .where(
      and_(
        models.Reservation.user_id == user_id,
        models.Reservation.reservation_status_id == 1
      )
    )
  )
  return result.all()


# -----------------------------------------------------------------
# GET ALL PENDING (used by COPY service for availability checks)
async def get_all_pending(db: AsyncSession) -> list[models.Reservation]:
  result = await db.execute(
    select(models.Reservation).where(models.Reservation.reservation_status_id == 1)
  )
  return list(result.scalars().all())


# -----------------------------------------------------------------
# EXISTS BY COPY ID
# Used by: copy/service.py - delete validation
async def exists_by_copy_id(db: AsyncSession, copy_id: int) -> bool:
  result = await db.execute(
    select(models.Reservation).where(models.Reservation.copy_id == copy_id)
  )
  return result.first() is not None