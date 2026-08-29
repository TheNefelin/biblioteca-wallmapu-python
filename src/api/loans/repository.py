from math import ceil
from datetime import date
from uuid import UUID
from sqlalchemy import and_, select, update as sa_update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import models
from src.schemas.dtos import PaginationRequestDTO, PaginationResponseDTO


def _loan_detail_options():
  return (
    selectinload(models.Loan.user),
    selectinload(models.Loan.copy)
      .selectinload(models.Copy.edition)
      .selectinload(models.Edition.book),
    selectinload(models.Loan.loan_status),
  )


# -----------------------------------------------------------------
# GET ALL PAGINATION
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  stmt = select(models.Loan).options(*_loan_detail_options())

  status_filter = pagination.filter.id_status if pagination.filter else None
  if status_filter and status_filter > 0:
    stmt = stmt.where(models.Loan.loan_status_id == status_filter)

  total_items_result = await db.execute(select(func.count()).select_from(stmt.subquery()))
  total_items = total_items_result.scalar_one()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0

  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (await db.execute(
    stmt
    .order_by(models.Loan.loan_date.desc())
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
# GET USER PAGINATION
async def get_all_pagination_by_user(db: AsyncSession, user_id: UUID, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  stmt = select(models.Loan).options(*_loan_detail_options()).where(models.Loan.user_id == user_id)

  status_filter = pagination.filter.id_status if pagination.filter else None
  if status_filter and status_filter > 0:
    stmt = stmt.where(models.Loan.loan_status_id == status_filter)

  total_items_result = await db.execute(select(func.count()).select_from(stmt.subquery()))
  total_items = total_items_result.scalar_one()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0

  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (await db.execute(
    stmt
    .order_by(models.Loan.loan_date.desc())
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
async def get_by_id(db: AsyncSession, id: int) -> models.Loan | None:
  result = await db.execute(
    select(models.Loan)
    .options(*_loan_detail_options())
    .where(models.Loan.id_loan == id)
  )
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# GET ALL OVERDUE
async def get_overdue(db: AsyncSession) -> list[models.Loan]:
  result = await db.execute(
    select(models.Loan)
    .options(
      selectinload(models.Loan.user),
      selectinload(models.Loan.copy),
      selectinload(models.Loan.loan_status)
    )
    .where(
      and_(
        models.Loan.due_date < date.today(),
        models.Loan.loan_status_id.in_([1, 3])
      )
    )
  )
  return list(result.scalars().all())


# -----------------------------------------------------------------
# GET ACTIVE LOAN BY COPY ID
async def get_active_loan_by_copy_id(db: AsyncSession, copy_id: int) -> models.Loan | None:
  result = await db.execute(
    select(models.Loan)
    .options(
      selectinload(models.Loan.user),
      selectinload(models.Loan.copy),
      selectinload(models.Loan.loan_status)
    )
    .where(
      and_(
        models.Loan.copy_id == copy_id,
        models.Loan.loan_status_id != 2
      )
    )
  )
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# GET ACTIVE LOANS BY BOOK ID
async def get_active_by_book_id(db: AsyncSession, book_id: int) -> list[models.Loan]:
  result = await db.execute(
    select(models.Loan)
    .join(models.Copy, models.Loan.copy_id == models.Copy.id_copy)
    .join(models.Edition, models.Copy.edition_id == models.Edition.id_edition)
    .options(
      selectinload(models.Loan.user),
      selectinload(models.Loan.copy),
      selectinload(models.Loan.loan_status)
    )
    .where(
      and_(
        models.Edition.book_id == book_id,
        models.Loan.loan_status_id == 1
      )
    )
  )
  return list(result.scalars().all())


# -----------------------------------------------------------------
# GET ACTIVE BY USER (returns tuples: id_loan, id_copy, book_id)
async def get_active_by_user(db: AsyncSession, user_id: UUID) -> list[tuple]:
  result = await db.execute(
    select(
      models.Loan.id_loan,
      models.Loan.copy_id,
      models.Edition.book_id
    )
    .join(models.Copy, models.Loan.copy_id == models.Copy.id_copy)
    .join(models.Edition, models.Copy.edition_id == models.Edition.id_edition)
    .where(
      and_(
        models.Loan.user_id == user_id,
        models.Loan.loan_status_id.in_([1, 3])
      )
    )
  )
  return result.all()


# -----------------------------------------------------------------
# GET ACTIVE LOAN BY BARCODE
async def get_active_by_barcode(db: AsyncSession, barcode: str) -> models.Loan | None:
  result = await db.execute(
    select(models.Loan)
    .options(*_loan_detail_options())
    .where(
      and_(
        models.Copy.barcode == barcode,
        models.Loan.loan_status_id.in_([1, 3])
      )
    )
    .join(models.Copy, models.Loan.copy_id == models.Copy.id_copy)
  )
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# GET ALL ACTIVE (used by COPY service for availability checks)
async def get_all_active(db: AsyncSession) -> list[models.Loan]:
  result = await db.execute(
    select(models.Loan)
    .where(models.Loan.loan_status_id.in_([1, 3]))
  )
  return list(result.scalars().all())


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, data: dict) -> models.Loan:
  item = models.Loan(**data)
  db.add(item)
  await db.commit()
  await db.refresh(item)
  return item


# -----------------------------------------------------------------
# GET OVERDUE LOAN COPY IDS
async def get_overdue_loan_copy_ids(db: AsyncSession) -> list[tuple[int, int]]:
  result = await db.execute(
    select(models.Loan.id_loan, models.Loan.copy_id)
    .where(
      and_(
        models.Loan.due_date < date.today(),
        models.Loan.loan_status_id == 1
      )
    )
  )
  return result.all()


# -----------------------------------------------------------------
# BULK UPDATE LOAN STATUS
async def bulk_update_loan_status(db: AsyncSession, loan_ids: list[int], status_id: int) -> int:
  result = await db.execute(
    sa_update(models.Loan)
    .where(models.Loan.id_loan.in_(loan_ids))
    .values(loan_status_id=status_id)
  )
  await db.commit()
  return result.rowcount


# -----------------------------------------------------------------
# BULK UPDATE COPY STATUS
async def bulk_update_copy_status(db: AsyncSession, copy_ids: list[int], status_id: int) -> int:
  result = await db.execute(
    sa_update(models.Copy)
    .where(models.Copy.id_copy.in_(copy_ids))
    .values(status_id=status_id)
  )
  await db.commit()
  return result.rowcount


# -----------------------------------------------------------------
# RETURN (actualiza campos de devoluciÃ³n)
async def return_loan(db: AsyncSession, loan_id: int, return_date: date, status_id: int) -> models.Loan | None:
  loan = (await db.execute(
    select(models.Loan).where(models.Loan.id_loan == loan_id)
  )).scalar_one_or_none()

  if loan:
    loan.return_date = return_date
    loan.loan_status_id = status_id
    await db.commit()
    await db.refresh(loan)
  return loan


# -----------------------------------------------------------------
# EXISTS BY COPY ID
# Used by: copy/service.py - delete validation
async def exists_by_copy_id(db: AsyncSession, copy_id: int) -> bool:
  result = await db.execute(
    select(models.Loan).where(models.Loan.copy_id == copy_id)
  )
  return result.first() is not None