from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import models


def get_all(db: Session) -> list[models.LoanPolicy]:
  try:
    return db.query(models.LoanPolicy).all()
  except SQLAlchemyError as e:
    raise e


def get_by_id(db: Session, id: int) -> models.LoanPolicy:
  try:
    return db.query(models.LoanPolicy).filter(models.LoanPolicy.id_policy == id).first()
  except SQLAlchemyError as e:
    raise e


def get_default_policy(db: Session) -> models.LoanPolicy:
  try:
    return db.query(models.LoanPolicy).first()
  except SQLAlchemyError as e:
    raise e


def create(db: Session, policy: models.LoanPolicy) -> models.LoanPolicy:
  try:
    db.add(policy)
    db.commit()
    db.refresh(policy)
    return policy
  except SQLAlchemyError as e:
    db.rollback()
    raise e


def update(db: Session, id: int, dto) -> models.LoanPolicy:
  try:
    policy = db.query(models.LoanPolicy).filter(models.LoanPolicy.id_policy == id).first()
    if policy:
      if dto.name is not None:
        policy.name = dto.name
      if dto.max_books is not None:
        policy.max_books = dto.max_books
      if dto.max_days is not None:
        policy.max_days = dto.max_days
      if dto.fine_per_day is not None:
        policy.fine_per_day = dto.fine_per_day
      if dto.reservation_days is not None:
        policy.reservation_days = dto.reservation_days
      db.commit()
      db.refresh(policy)
    return policy
  except SQLAlchemyError as e:
    db.rollback()
    raise e


def delete(db: Session, id: int) -> bool:
  try:
    policy = db.query(models.LoanPolicy).filter(models.LoanPolicy.id_policy == id).first()
    if policy:
      db.delete(policy)
      db.commit()
      return True
    return None
  except SQLAlchemyError as e:
    db.rollback()
    raise e
