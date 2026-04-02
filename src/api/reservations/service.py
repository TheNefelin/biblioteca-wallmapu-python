from datetime import datetime, timedelta, date
from uuid import UUID
from sqlalchemy.orm import Session
from . import dtos, repository, models
from src.api.loans.repository import create as create_loan
from src.api.copy.models import Copy


def get_all(db: Session) -> list[dtos.ReservationDetailDTO]:
  reservations = repository.get_all(db)
  return [_to_detail_dto(r) for r in reservations]


def get_by_id(db: Session, id: int) -> dtos.ReservationDetailDTO:
  reservation = repository.get_by_id(db, id)
  if not reservation:
    return None
  return _to_detail_dto(reservation)


def get_by_user_id(db: Session, user_id: UUID) -> list[dtos.ReservationDetailDTO]:
  reservations = repository.get_by_user_id(db, user_id)
  return [_to_detail_dto(r) for r in reservations]


def get_active_by_copy_id(db: Session, copy_id: int) -> list[dtos.ReservationDetailDTO]:
  reservations = repository.get_active_by_copy_id(db, copy_id)
  return [_to_detail_dto(r) for r in reservations]


def create(db: Session, user_id: UUID, dto: dtos.CreateReservationDTO) -> dtos.ReservationDetailDTO:
  copy = db.query(Copy).filter(Copy.id_copy == dto.copy_id).first()
  if not copy:
    raise ValueError("Ejemplar no encontrado")

  if copy.status_id != 1:
    raise ValueError("El ejemplar no está disponible")

  existing = repository.get_active_by_user_and_copy(db, user_id, dto.copy_id)
  if existing:
    raise ValueError("Ya tienes una reserva activa para este ejemplar")

  reservation_days = _get_reservation_days(db)
  expiration_date = datetime.now() + timedelta(days=reservation_days)

  reservation = models.Reservation(
    user_id=user_id,
    copy_id=dto.copy_id,
    expiration_date=expiration_date,
    reservation_status_id=1
  )

  created = repository.create(db, reservation)
  return get_by_id(db, created.id_reservation)


def mark_as_pickup(db: Session, id: int, copy_id: int) -> dtos.ReservationDetailDTO:
  reservation = repository.get_by_id(db, id)
  if not reservation:
    return None

  if reservation.reservation_status_id != 1:
    raise ValueError("Solo se puede marcar como retirada una reserva pendiente")

  if reservation.expiration_date < datetime.now():
    raise ValueError("No se puede entregar una reserva vencida. Debe generar una nueva.")

  copy = db.query(Copy).filter(Copy.id_copy == copy_id).first()
  if not copy:
    raise ValueError("Ejemplar no encontrado")

  if copy.status_id != 1:
    raise ValueError("El ejemplar no está disponible")

  from src.api.loans.models import Loan
  max_days = _get_max_loan_days(db)
  due_date = date.today() + timedelta(days=max_days)

  loan = Loan(
    copy_id=copy.id_copy,
    user_id=reservation.user_id,
    loan_date=date.today(),
    due_date=due_date,
    status="active"
  )
  create_loan(db, loan)

  copy.status_id = 2
  db.commit()

  repository.update_status(db, id, 2)
  return get_by_id(db, id)


def mark_as_cancelled(db: Session, id: int) -> dtos.ReservationDetailDTO:
  reservation = repository.get_by_id(db, id)
  if not reservation:
    return None

  if reservation.reservation_status_id != 1:
    raise ValueError("Solo se puede cancelar una reserva pendiente")

  repository.update_status(db, id, 3)
  return get_by_id(db, id)


def mark_as_expired(db: Session, id: int) -> dtos.ReservationDetailDTO:
  reservation = repository.get_by_id(db, id)
  if not reservation:
    return None

  if reservation.reservation_status_id != 1:
    raise ValueError("Solo se puede marcar como vencida una reserva pendiente")

  repository.update_status(db, id, 4)
  return get_by_id(db, id)


def expire_overdue_reservations(db: Session) -> int:
  expired = repository.get_expired(db)
  count = 0
  for reservation in expired:
    repository.update_status(db, reservation.id_reservation, 4)
    count += 1
  return count


def delete(db: Session, id: int) -> bool:
  reservation = repository.get_by_id(db, id)
  if not reservation:
    return None
  return repository.delete(db, id)


def _to_detail_dto(reservation: models.Reservation) -> dtos.ReservationDetailDTO:
  copy = reservation.copy
  book = copy.edition.book if copy and copy.edition else None
  
  return dtos.ReservationDetailDTO(
    id_reservation=reservation.id_reservation,
    reservation_date=reservation.reservation_date,
    expiration_date=reservation.expiration_date,
    user_id=reservation.user_id,
    user_name=reservation.user.name if reservation.user else None,
    user_lastname=reservation.user.lastname if reservation.user else None,
    user_email=reservation.user.email if reservation.user else None,
    copy_id=copy.id_copy if copy else None,
    copy_barcode=str(copy.barcode) if copy else None,
    copy_signature=copy.signature_topography if copy else None,
    book_id=book.id_book if book else None,
    book_title=book.title if book else None,
    reservation_status_id=reservation.reservation_status_id,
    reservation_status_name=reservation.status.status if reservation.status else None
  )


def _get_reservation_days(db: Session) -> int:
  from src.api.loan_policies.repository import get_default_policy
  policy = get_default_policy(db)
  return policy.reservation_days if policy else 3


def _get_max_loan_days(db: Session) -> int:
  from src.api.loan_policies.repository import get_default_policy
  policy = get_default_policy(db)
  return policy.max_days if policy else 14
