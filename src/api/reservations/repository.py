from uuid import UUID
from math import ceil
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from src.api.copy.models import Copy
from src.api.editions.models import Edition
from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models


def get_all_pagination(pagination: PaginationRequestDTO, db: Session) -> PaginationResponseDTO:
  try:
    query = (
      db.query(models.Reservation)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.copy).joinedload(Copy.edition).joinedload(Edition.book),
        joinedload(models.Reservation.status)
      )
    )

    # Filtrar por status (0 = todos)
    status_filter = pagination.filter.id_status if pagination.filter else None
    if status_filter and status_filter > 0:
      query = query.filter(
        models.Reservation.reservation_status_id == status_filter
      )

    total_items = query.count()
    total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0

    page = min(pagination.page, total_pages) if total_pages > 0 else 1
    offset = (page - 1) * pagination.limit

    result = (
      query
      .order_by(models.Reservation.reservation_date.desc())
      .offset(offset)
      .limit(pagination.limit)
      .all()
    )

    next_url = f"/api/reservations/pagination?page={page + 1}&limit={pagination.limit}" if page < total_pages else None
    prev_url = f"/api/reservations/pagination?page={page - 1}&limit={pagination.limit}" if page > 1 else None

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
    

def get_all(db: Session) -> list[models.Reservation]:
  try:
    return (
      db.query(models.Reservation)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.copy).joinedload(Copy.edition).joinedload(Edition.book),
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
        joinedload(models.Reservation.copy).joinedload(Copy.edition).joinedload(Edition.book),
        joinedload(models.Reservation.status)
      )
      .filter(models.Reservation.id_reservation == id)
      .first()
    )
  except SQLAlchemyError as e:
    raise e


def get_by_user_id(db: Session, user_id: UUID) -> list[models.Reservation]:
  try:
    return (
      db.query(models.Reservation)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.copy).joinedload(Copy.edition).joinedload(Edition.book),
        joinedload(models.Reservation.status)
      )
      .filter(models.Reservation.user_id == user_id)
      .order_by(models.Reservation.reservation_date.desc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e


def get_active_by_user_and_copy(db: Session, user_id: UUID, copy_id: int) -> models.Reservation:
  try:
    return (
      db.query(models.Reservation)
      .filter(
        and_(
          models.Reservation.user_id == user_id,
          models.Reservation.copy_id == copy_id,
          models.Reservation.reservation_status_id == 1
        )
      )
      .first()
    )
  except SQLAlchemyError as e:
    raise e


def get_active_by_copy_id(db: Session, copy_id: int) -> list[models.Reservation]:
  try:
    return (
      db.query(models.Reservation)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.copy),
        joinedload(models.Reservation.status)
      )
      .filter(
        and_(
          models.Reservation.copy_id == copy_id,
          models.Reservation.reservation_status_id == 1
        )
      )
      .order_by(models.Reservation.reservation_date.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e


def get_active_reservation_by_copy_id(db: Session, copy_id: int) -> models.Reservation | None:
  try:
    return (
      db.query(models.Reservation)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.copy),
        joinedload(models.Reservation.status)
      )
      .filter(
        and_(
          models.Reservation.copy_id == copy_id,
          models.Reservation.reservation_status_id == 1
        )
      )
      .order_by(models.Reservation.reservation_date.asc())
      .first()
    )
  except SQLAlchemyError as e:
    raise e


def get_active_by_book_id(db: Session, book_id: int) -> list[models.Reservation]:
  try:
    from src.api.copy.models import Copy
    from src.api.editions.models import Edition
    
    return (
      db.query(models.Reservation)
      .join(Copy, models.Reservation.copy_id == Copy.id_copy)
      .join(Edition, Copy.edition_id == Edition.id_edition)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.copy),
        joinedload(models.Reservation.status)
      )
      .filter(
        and_(
          Edition.book_id == book_id,
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
        joinedload(models.Reservation.copy),
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
