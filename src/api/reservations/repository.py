from uuid import UUID
from math import ceil
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
      db.query(models.Reservation)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.copy)
          .joinedload(copy_models.Copy.edition)
          .joinedload(edition_models.Edition.book),
        joinedload(models.Reservation.status)
      )
    )

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


# -----------------------------------------------------------------
# GET USER PAGINATION
def get_all_pagination_by_user(db: Session, user_id: UUID, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  try:
    query = (
      db.query(models.Reservation)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.copy)
          .joinedload(copy_models.Copy.edition)
          .joinedload(edition_models.Edition.book),
        joinedload(models.Reservation.status)
      )
      .filter(models.Reservation.user_id == user_id)
    )

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

    next_url = f"/api/reservations/pagination/user?page={page + 1}&limit={pagination.limit}" if page < total_pages else None
    prev_url = f"/api/reservations/pagination/user?page={page - 1}&limit={pagination.limit}" if page > 1 else None

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
# GET BY ID
def get_by_id(db: Session, id: int) -> models.Reservation:
  try:
    return (
      db.query(models.Reservation)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.copy)
          .joinedload(copy_models.Copy.edition)
          .joinedload(edition_models.Edition.book),
        joinedload(models.Reservation.status)
      )
      .filter(models.Reservation.id_reservation == id)
      .first()
    )
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# UPDATE RESERVATION STATUS
def update_status(db: Session, id: int, status_id: int) -> models.Reservation:
  try:
    reservation = (
      db.query(models.Reservation)
      .filter(models.Reservation.id_reservation == id)
      .first()
    )
    
    if reservation:
      reservation.reservation_status_id = status_id
      db.commit()
      db.refresh(reservation)
    
    return reservation
  except SQLAlchemyError as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# UPDATE - EXPIRE OVERDUE (Bulk update como Loan)
def expire_overdue_as_expired(db: Session) -> int:
  try:
    from datetime import datetime
    result = (
      db.query(models.Reservation)
      .filter(
        and_(
          models.Reservation.reservation_status_id == 1,
          models.Reservation.expiration_date < datetime.now()
        )
      )
      .update({"reservation_status_id": 4})
    )
    db.commit()
    return result
  except SQLAlchemyError as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# CREATE
def create(db: Session, data: dict) -> models.Reservation:
  try:
    item = models.Reservation(**data)

    db.add(item)
    db.commit()
    db.refresh(item)
    
    return item
  except SQLAlchemyError as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# GET ACTIVE RESERVATIONS BY BOOK ID
def get_active_by_book_id(db: Session, book_id: int) -> list[models.Reservation]:
  try:
    return (
      db.query(models.Reservation)
      .join(copy_models.Copy, models.Reservation.copy_id == copy_models.Copy.id_copy)
      .join(edition_models.Edition, copy_models.Copy.edition_id == edition_models.Edition.id_edition)
      .options(
        joinedload(models.Reservation.user),
        joinedload(models.Reservation.copy),
        joinedload(models.Reservation.status)
      )
      .filter(
        and_(
          edition_models.Edition.book_id == book_id,
          models.Reservation.reservation_status_id == 1
        )
      )
      .order_by(models.Reservation.reservation_date.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# GET ACTIVE RESERVATIONS BY USER (returns tuples: id_reservation, id_copy, book_id)
def get_active_by_user(db: Session, user_id: UUID) -> list[tuple]:
  """Retorna lista de (id_reservation, id_copy, book_id) activas del usuario"""
  try:
    return (
      db.query(
        models.Reservation.id_reservation,
        models.Reservation.copy_id,
        edition_models.Edition.book_id
      )
      .join(copy_models.Copy, models.Reservation.copy_id == copy_models.Copy.id_copy)
      .join(edition_models.Edition, copy_models.Copy.edition_id == edition_models.Edition.id_edition)
      .filter(
        and_(
          models.Reservation.user_id == user_id,
          models.Reservation.reservation_status_id == 1
        )
      )
      .all()
    )
  except SQLAlchemyError as e:
    raise e
