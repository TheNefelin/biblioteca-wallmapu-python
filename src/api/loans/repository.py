from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from . import models


def get_all(db: Session) -> list[models.Loan]:
  try:
    return (
      db.query(models.Loan)
      .options(
        joinedload(models.Loan.user),
        joinedload(models.Loan.copy)
      )
      .order_by(models.Loan.loan_date.desc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e


def get_by_id(db: Session, id: int) -> models.Loan:
  try:
    return (
      db.query(models.Loan)
      .options(
        joinedload(models.Loan.user),
        joinedload(models.Loan.copy)
      )
      .filter(models.Loan.id_loan == id)
      .first()
    )
  except SQLAlchemyError as e:
    raise e


def get_active_by_user_id(db: Session, user_id: str) -> list[models.Loan]:
  try:
    return (
      db.query(models.Loan)
      .options(
        joinedload(models.Loan.user),
        joinedload(models.Loan.copy)
      )
      .filter(
        and_(
          models.Loan.user_id == user_id,
          models.Loan.status.in_(["active", "overdue"])
        )
      )
      .all()
    )
  except SQLAlchemyError as e:
    raise e


def get_active_by_book_id(db: Session, book_id: int) -> list[models.Loan]:
  try:
    from src.api.copy.models import Copy
    from src.api.editions.models import Edition
    return (
      db.query(models.Loan)
      .join(Copy)
      .join(Edition)
      .options(
        joinedload(models.Loan.user),
        joinedload(models.Loan.copy)
      )
      .filter(
        and_(
          Edition.book_id == book_id,
          models.Loan.status.in_(["active", "overdue"])
        )
      )
      .all()
    )
  except SQLAlchemyError as e:
    raise e


def get_overdue(db: Session) -> list[models.Loan]:
  try:
    from datetime import date
    return (
      db.query(models.Loan)
      .options(
        joinedload(models.Loan.user),
        joinedload(models.Loan.copy)
      )
      .filter(
        and_(
          models.Loan.due_date < date.today(),
          models.Loan.status == "active"
        )
      )
      .all()
    )
  except SQLAlchemyError as e:
    raise e


def create(db: Session, loan: models.Loan) -> models.Loan:
  try:
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan
  except SQLAlchemyError as e:
    db.rollback()
    raise e


def update_status(db: Session, id: int, status: str) -> models.Loan:
  try:
    loan = db.query(models.Loan).filter(models.Loan.id_loan == id).first()
    if loan:
      loan.status = status
      db.commit()
      db.refresh(loan)
    return loan
  except SQLAlchemyError as e:
    db.rollback()
    raise e


def return_loan(db: Session, id: int, return_date) -> models.Loan:
  try:
    loan = db.query(models.Loan).filter(models.Loan.id_loan == id).first()
    if loan:
      loan.return_date = return_date
      loan.status = "returned"
      db.commit()
      db.refresh(loan)
    return loan
  except SQLAlchemyError as e:
    db.rollback()
    raise e


def mark_overdue_as_overdue(db: Session) -> int:
  try:
    from datetime import date
    result = (
      db.query(models.Loan)
      .filter(
        and_(
          models.Loan.due_date < date.today(),
          models.Loan.status == "active"
        )
      )
      .update({"status": "overdue"})
    )
    db.commit()
    return result
  except SQLAlchemyError as e:
    db.rollback()
    raise e
