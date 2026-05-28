from math import ceil
from datetime import date
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from src.api.editions import models as edition_models
from src.api.copy import models as copy_models
from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  query = (
    db.query(models.Loan)
    .options(
      joinedload(models.Loan.user),
      joinedload(models.Loan.copy)
        .joinedload(copy_models.Copy.edition)
        .joinedload(edition_models.Edition.book),
      joinedload(models.Loan.loan_status),
    )
  )

  status_filter = pagination.filter.id_status if pagination.filter else None
  if status_filter and status_filter > 0:
    query = query.filter(
      models.Loan.loan_status_id == status_filter
    )

  total_items = query.count()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0

  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (
    query
    .order_by(models.Loan.loan_date.desc())
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
    prev=None
  )


# -----------------------------------------------------------------
# GET USER PAGINATION
def get_all_pagination_by_user(db: Session, user_id: UUID, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  query = (
    db.query(models.Loan)
    .options(
      joinedload(models.Loan.user),
      joinedload(models.Loan.copy)
        .joinedload(copy_models.Copy.edition)
        .joinedload(edition_models.Edition.book),
      joinedload(models.Loan.loan_status),
    )
    .filter(models.Loan.user_id == user_id)
  )

  status_filter = pagination.filter.id_status if pagination.filter else None
  if status_filter and status_filter > 0:
    query = query.filter(
      models.Loan.loan_status_id == status_filter
    )

  total_items = query.count()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0

  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (
    query
    .order_by(models.Loan.loan_date.desc())
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
    prev=None
  )


# -----------------------------------------------------------------
# GET BY ID
def get_by_id(db: Session, id: int) -> models.Loan | None:
  return (
    db.query(models.Loan)
    .options(
      joinedload(models.Loan.user),
      joinedload(models.Loan.copy)
        .joinedload(copy_models.Copy.edition)
        .joinedload(edition_models.Edition.book),
      joinedload(models.Loan.loan_status),
    )
    .filter(models.Loan.id_loan == id)
    .first()
  )


# -----------------------------------------------------------------
# GET ALL OVERDUE
def get_overdue(db: Session) -> list[models.Loan]:
  return (
    db.query(models.Loan)
    .options(
      joinedload(models.Loan.user),
      joinedload(models.Loan.copy),
      joinedload(models.Loan.loan_status)
    )
    .filter(
      and_(
        models.Loan.due_date < date.today(),
        models.Loan.loan_status_id.in_([1, 3])
      )
    )
    .all()
  )


# -----------------------------------------------------------------
# GET ACTIVE LOAN BY COPY ID
def get_active_loan_by_copy_id(db: Session, copy_id: int) -> models.Loan | None:
  return (
    db.query(models.Loan)
    .options(
      joinedload(models.Loan.user),
      joinedload(models.Loan.copy),
      joinedload(models.Loan.loan_status)
    )
    .filter(
      and_(
        models.Loan.copy_id == copy_id,
        models.Loan.loan_status_id != 2
      )
    )
    .first()
  )


# -----------------------------------------------------------------
# GET ACTIVE LOANS BY BOOK ID
def get_active_by_book_id(db: Session, book_id: int) -> list[models.Loan]:
  return (
    db.query(models.Loan)
    .join(copy_models.Copy, models.Loan.copy_id == copy_models.Copy.id_copy)
    .join(edition_models.Edition, copy_models.Copy.edition_id == edition_models.Edition.id_edition)
    .options(
      joinedload(models.Loan.user),
      joinedload(models.Loan.copy),
      joinedload(models.Loan.loan_status)
    )
    .filter(
      and_(
        edition_models.Edition.book_id == book_id,
        models.Loan.loan_status_id == 1
      )
    )
    .all()
  )


# -----------------------------------------------------------------
# GET ACTIVE BY USER (returns tuples: id_loan, id_copy, book_id)
def get_active_by_user(db: Session, user_id: UUID) -> list[tuple]:
  return (
    db.query(
      models.Loan.id_loan,
      models.Loan.copy_id,
      edition_models.Edition.book_id
    )
    .join(copy_models.Copy, models.Loan.copy_id == copy_models.Copy.id_copy)
    .join(edition_models.Edition, copy_models.Copy.edition_id == edition_models.Edition.id_edition)
    .filter(
      and_(
        models.Loan.user_id == user_id,
        models.Loan.loan_status_id.in_([1, 3])
      )
    )
    .all()
  )


# -----------------------------------------------------------------
# GET ACTIVE LOAN BY BARCODE
def get_active_by_barcode(db: Session, barcode: str) -> models.Loan | None:
  return (
    db.query(models.Loan)
    .options(
      joinedload(models.Loan.user),
      joinedload(models.Loan.copy)
        .joinedload(copy_models.Copy.edition)
        .joinedload(edition_models.Edition.book),
      joinedload(models.Loan.loan_status),
    )
    .filter(
      and_(
        copy_models.Copy.barcode == barcode,
        models.Loan.loan_status_id.in_([1, 3])
      )
    )
    .first()
  )


# -----------------------------------------------------------------
# GET ALL ACTIVE (used by COPY service for availability checks)
def get_all_active(db: Session) -> list[models.Loan]:
  return (
      db.query(models.Loan)
      .filter(models.Loan.loan_status_id.in_([1, 3]))
      .all()
  )


# -----------------------------------------------------------------
# CREATE
def create(db: Session, data: dict) -> models.Loan:
  item = models.Loan(**data)
  db.add(item)
  db.commit()
  db.refresh(item)

  return item


# -----------------------------------------------------------------
# GET OVERDUE LOAN COPY IDS
def get_overdue_loan_copy_ids(db: Session) -> list[tuple[int, int]]:
  return [
    (row.id_loan, row.copy_id)
    for row in db.query(models.Loan.id_loan, models.Loan.copy_id)
    .filter(
      and_(
        models.Loan.due_date < date.today(),
        models.Loan.loan_status_id == 1
      )
    )
    .all()
  ]


# -----------------------------------------------------------------
# BULK UPDATE LOAN STATUS
def bulk_update_loan_status(db: Session, loan_ids: list[int], status_id: int) -> int:
  result = (
    db.query(models.Loan)
    .filter(models.Loan.id_loan.in_(loan_ids))
    .update({"loan_status_id": status_id})
  )
  db.commit()
  return result


# -----------------------------------------------------------------
# BULK UPDATE COPY STATUS
def bulk_update_copy_status(db: Session, copy_ids: list[int], status_id: int) -> int:
  result = (
    db.query(copy_models.Copy)
    .filter(copy_models.Copy.id_copy.in_(copy_ids))
    .update({"status_id": status_id}, synchronize_session=False)
  )
  db.commit()
  return result


# -----------------------------------------------------------------
# RETURN (actualiza campos de devolución)
def return_loan(db: Session, loan_id: int, return_date: date, status_id: int) -> models.Loan | None:
  loan = (
    db.query(models.Loan)
    .filter(models.Loan.id_loan == loan_id)
    .first()
  )
  
  if loan:
    loan.return_date = return_date
    loan.loan_status_id = status_id
    db.commit()
    db.refresh(loan)
  return loan


# -----------------------------------------------------------------
# EXISTS BY COPY ID
# Used by: copy/service.py - delete validation
def exists_by_copy_id(db: Session, copy_id: int) -> bool:
  return db.query(models.Loan).filter(models.Loan.copy_id == copy_id).first() is not None