from math import ceil
from datetime import date
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_


from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(pagination: PaginationRequestDTO, db: Session) -> PaginationResponseDTO:
  try:
    query = (
      db.query(models.Loan)
      .options(
        joinedload(models.Loan.user),
        joinedload(models.Loan.copy),
        joinedload(models.Loan.loan_status)
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
          models.Loan.loan_status_id == 1
        )
      )
      .all()
    )
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# GET BY ID
def get_by_id(db: Session, id: int) -> models.Loan | None:
  try:
    return (
      db.query(models.Loan)
      .options(
        joinedload(models.Loan.user),
        joinedload(models.Loan.copy),
        joinedload(models.Loan.loan_status)
      )
      .filter(models.Loan.id_loan == id)
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
def return_loan(db: Session, id: int, return_date) -> models.Loan:
  try:
    loan = db.query(models.Loan).filter(models.Loan.id_loan == id).first()
    if loan:
      loan.return_date = return_date
      loan.loan_status_id = 2
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

