from math import ceil
from datetime import date
from uuid import UUID
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_

from src.api.editions import models as edition_models
from src.api.copy import models as copy_models
from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  try:
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

    next_url = f"/api/loans/pagination?page={page + 1}&limit={pagination.limit}" if page < total_pages else None
    prev_url = f"/api/loans/pagination?page={page - 1}&limit={pagination.limit}" if page > 1 else None

    return PaginationResponseDTO(
      page=page,
      pages=total_pages,
      items=total_items,
      data=result,
      next=next_url,
      prev=prev_url
    )
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# GET USER PAGINATION
def get_all_pagination_by_user(db: Session, user_id: UUID, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  try:
    query = (
      db.query(models.Loan)
      .options(
        joinedload(models.Loan.user),
        joinedload(models.Loan.copy)
          .joinedload(copy_models.Copy.edition)
          .joinedload(edition_models.Edition.book),
        joinedload(models.Loan.loan_status)
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

    next_url = f"/api/loans/pagination?page={page + 1}&limit={pagination.limit}" if page < total_pages else None
    prev_url = f"/api/loans/pagination?page={page - 1}&limit={pagination.limit}" if page > 1 else None

    return PaginationResponseDTO(
      page=page,
      pages=total_pages,
      items=total_items,
      data=result,
      next=next_url,
      prev=prev_url
    )
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# GET ALL OVERDUE
def get_overdue(db: Session) -> list[models.Loan]:
  try:    
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
          models.Loan.loan_status_id.in_([1, 3])  # 1=activo, 3=vencido
        )
      )
      .all()
    )
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# GET ACTIVE LOAN BY COPY ID
def get_active_loan_by_copy_id(db: Session, copy_id: int) -> models.Loan | None:
  try:
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
          models.Loan.loan_status_id == 1
        )
      )
      .first()
    )
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# GET ACTIVE LOANS BY BOOK ID
def get_active_by_book_id(db: Session, book_id: int) -> list[models.Loan]:
  try:
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
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# GET ACTIVE LOAN BY BARCODE
def get_active_by_barcode(db: Session, barcode: str) -> models.Loan | None:
  """
  Busca préstamo activo por barcode del ejemplar.
  Retorna el loan activo (status_id=1) linked al barcode.
  """
  try:
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
          models.Loan.loan_status_id == 1  # Solo préstamos activos
        )
      )
      .first()
    )
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# CREATE
def create(db: Session, loan: models.Loan) -> models.Loan:
  try:
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan
  except SQLAlchemyError as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# RETURN
def return_loan(db: Session, loan_id: int) -> models.Loan:
  try:
    loan = db.query(models.Loan).filter(models.Loan.id_loan == loan_id).first()
    if loan:
      loan.return_date = date.today()
      loan.loan_status_id = 2
      
      copy = db.query(copy_models.Copy).filter(copy_models.Copy.id_copy == loan.copy_id).first()
      if copy:
        copy.status_id = 1
      
      db.commit()
      db.refresh(loan)
    return loan
  except SQLAlchemyError as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# UPDATE - EXPIRE OVERDUE
def expire_overdue_as_overdue(db: Session) -> int:
  try:
    result = (
      db.query(models.Loan)
      .filter(
        and_(
          models.Loan.due_date < date.today(),
          models.Loan.loan_status_id == 1
        )
      )
      .update({"loan_status_id": 3})
    )
    db.commit()
    return result
  except SQLAlchemyError as e:
    db.rollback()
    raise e

