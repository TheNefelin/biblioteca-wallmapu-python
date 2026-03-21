from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from . import models


def get_all(db: Session) -> list[models.Reservation]:
  try:
    return (
      db.query(models.Reservation)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.book),
        joinedload(models.Reservation.status)
      )
      .order_by(models.Reservation.reservation_date.desc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e


def get_by_id(db: Session, id: int) -> models.Reservation:
  try:
    return (
      db.query(models.Reservation)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.book),
        joinedload(models.Reservation.status)
      )
      .filter(models.Reservation.id_reservation == id)
      .first()
    )
  except SQLAlchemyError as e:
    raise e


def get_by_user_id(db: Session, user_id: str) -> list[models.Reservation]:
  try:
    return (
      db.query(models.Reservation)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.book),
        joinedload(models.Reservation.status)
      )
      .filter(models.Reservation.user_id == user_id)
      .order_by(models.Reservation.reservation_date.desc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e


def get_active_by_user_and_book(db: Session, user_id: str, book_id: int) -> models.Reservation:
  try:
    return (
      db.query(models.Reservation)
      .filter(
        and_(
          models.Reservation.user_id == user_id,
          models.Reservation.book_id == book_id,
          models.Reservation.reservation_status_id == 1
        )
      )
      .first()
    )
  except SQLAlchemyError as e:
    raise e


def get_active_by_book_id(db: Session, book_id: int) -> list[models.Reservation]:
  try:
    return (
      db.query(models.Reservation)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.book),
        joinedload(models.Reservation.status)
      )
      .filter(
        and_(
          models.Reservation.book_id == book_id,
          models.Reservation.reservation_status_id == 1
        )
      )
      .order_by(models.Reservation.reservation_date.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e


def get_expired(db: Session) -> list[models.Reservation]:
  try:
    from datetime import datetime
    return (
      db.query(models.Reservation)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.book),
        joinedload(models.Reservation.status)
      )
      .filter(
        and_(
          models.Reservation.reservation_status_id == 1,
          models.Reservation.expiration_date < datetime.now()
        )
      )
      .all()
    )
  except SQLAlchemyError as e:
    raise e


def create(db: Session, reservation: models.Reservation) -> models.Reservation:
  try:
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation
  except SQLAlchemyError as e:
    db.rollback()
    raise e


def update_status(db: Session, id: int, status_id: int) -> models.Reservation:
  try:
    reservation = db.query(models.Reservation).filter(models.Reservation.id_reservation == id).first()
    if reservation:
      reservation.reservation_status_id = status_id
      db.commit()
      db.refresh(reservation)
    return reservation
  except SQLAlchemyError as e:
    db.rollback()
    raise e


def delete(db: Session, id: int) -> bool:
  try:
    reservation = db.query(models.Reservation).filter(models.Reservation.id_reservation == id).first()
    if reservation:
      db.delete(reservation)
      db.commit()
      return True
    return None
  except SQLAlchemyError as e:
    db.rollback()
    raise e
