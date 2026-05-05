from datetime import datetime, timedelta, date
from uuid import UUID
from sqlalchemy.orm import Session
import logging

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.api.loan_policies import repository as loan_policy_repository
from src.api.loans import repository as loan_repository, service as loan_service, dtos as loan_dtos
from src.api.copy import repository as copy_repository
from src.api.notifications import dtos as notification_dtos, service as notification_service
from src.services import email_service
from . import dtos, repository, models

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------
# HELPER - Mapea entidad a DTO con relaciones
def _map_reservation_to_detail(reservation: models.Reservation) -> dtos.ReservationDetailDTO:
  copy = reservation.copy
  book = copy.edition.book if copy and copy.edition else None
  
  return dtos.ReservationDetailDTO(
    id_reservation=reservation.id_reservation,
    reservation_date=reservation.reservation_date,
    expiration_date=reservation.expiration_date,
    user_id=reservation.user_id,
    user_name=reservation.user.name if reservation.user else "",
    user_lastname=reservation.user.lastname if reservation.user else "",
    user_email=reservation.user.email if reservation.user else "",
    copy_id=copy.id_copy if copy else 0,
    copy_barcode=str(copy.barcode) if copy else "",
    copy_signature=copy.signature_topography if copy else "",
    book_id=book.id_book if book else 0,
    book_title=book.title if book else "",
    reservation_status_id=reservation.reservation_status_id,
    reservation_status_name=reservation.status.name if reservation.status else ""
  )


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  page = repository.get_all_pagination(db, pagination)
  return PaginationResponseDTO(
    page=page.page,
    pages=page.pages,
    items=page.items,
    data=[_map_reservation_to_detail(r) for r in page.data],
    next=page.next,
    prev=page.prev,
  )


# -----------------------------------------------------------------
# GET USER PAGINATION
def get_all_pagination_by_user(db: Session, user_id: UUID, pagination: PaginationRequestDTO):
  page = repository.get_all_pagination_by_user(db, user_id, pagination)
  return PaginationResponseDTO(
    page=page.page,
    pages=page.pages,
    items=page.items,
    data=[_map_reservation_to_detail(r) for r in page.data],
    next=page.next,
    prev=page.prev,
  )


# -----------------------------------------------------------------
# GET BY ID
def get_by_id(db: Session, id: int) -> dtos.ReservationDetailDTO | None:
  reservation = repository.get_by_id(db, id)
  
  if not reservation:
    return None

  return _map_reservation_to_detail(reservation)


# -----------------------------------------------------------------
# CREATE
def create(db: Session, user_id: UUID, dto: dtos.CreateReservationDTO) -> dtos.ReservationDetailDTO:
  try:
    copy = copy_repository.get_by_id(db, dto.copy_id)
    book_id = copy.edition.book_id

    if not copy:
      raise ValueError("Ejemplar no encontrado")

    if int(copy.status_id) != 1:
      raise ValueError("El ejemplar no está disponible")

    loan_policy = loan_policy_repository.get_default_policy(db)
    reservation_days = int(loan_policy.reservation_days)
    expiration_date = date.today() + timedelta(days=reservation_days)

    # Obtener reservas y préstamos activos del usuario (2 consultas eficientes)
    active_reservations = repository.get_active_by_user(db, user_id)  # (id_reservation, id_copy, book_id)
    active_loans = loan_repository.get_active_by_user(db, user_id)  # (id_loan, id_copy, book_id)

    # 1. Validar límite de Loan Policies (3 libros max entre reservas y préstamos)
    total = len(active_reservations) + len(active_loans)

    if total >= loan_policy.max_books:
      raise ValueError("Has alcanzado el límite máximo de reservas y/o préstamos de libros")

    # 2. Validar que el libro NO esté ya en reservas o préstamos activos
    book_in_reservations = any(r[2] == book_id for r in active_reservations)  # r[2] = book_id
    book_in_loans = any(l[2] == book_id for l in active_loans)  # l[2] = book_id

    if book_in_reservations or book_in_loans:
      raise ValueError("Ya tienes este libro reservado o prestado")

    reservation_dto = dtos.ReservationDTO(
      user_id=user_id,
      copy_id=dto.copy_id,
      expiration_date=expiration_date
    )

    # Crear Reserva
    created = repository.create(db, reservation_dto.model_dump(exclude_none=True))

    if not created or not created.id_reservation:
      raise ValueError("Error al crear la reserva")

    # Disparar notificación (efecto secundario resiliente)
    notification_service.create_notification_for_reservation_and_send_email(db, created.id_reservation)

    return get_by_id(db, int(created.id_reservation))
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# UPDATE - CANCEL
def mark_as_cancelled(db: Session, id: int):
  try:
    reservation = repository.get_by_id(db, id)
    
    if not reservation:
      return None

    if int(reservation.reservation_status_id) != 1:
      raise ValueError("Solo se puede cancelar una reserva pendiente")

    # Actualiza Reserva
    updated = repository.update_status(db, id, 3)

    # Disparar notificación (efecto secundario resiliente)
    notification_service.cancel_notification_for_reservation_and_send_email(db, updated.id_reservation)

    return get_by_id(db, id)
  except Exception as e:
    raise e

# -----------------------------------------------------------------
# UPDATE - MARK AS PICKUP AND CREATE LOAN
def mark_as_pickup(db: Session, id: int, copy_id: int):
  reservation = repository.get_by_id(db, id)
  if not reservation:
    return None

  if int(reservation.reservation_status_id) != 1:
    raise ValueError("Solo se puede marcar como retirada una reserva pendiente")

  if reservation.expiration_date < datetime.now():
    raise ValueError("No se puede entregar una reserva vencida. Debe generar una nueva.")

  copy = copy_repository.get_by_id(db, copy_id)
  if not copy:
    raise ValueError("Ejemplar no encontrado")

  if int(copy.status_id) != 1:
    raise ValueError("El ejemplar no está disponible")

  loan_policy = loan_policy_repository.get_default_policy(db)
  max_days = int(loan_policy.max_days)
  due_date = date.today() + timedelta(days=max_days)

  loan_dto = loan_dtos.CreateLoanDTO(
    copy_id=copy.id_copy,
    user_id=reservation.user_id,
  )

  loan_service.create(db, loan_dto)
  repository.update_status(db, id, 2)

  # Notificación resiliente
  try:
    notification_dto = notification_dtos.CreateNotificationDTO(
      title="RESERVA LISTA",
      message=f"Reserva #{id} lista para retiro. Préstamo creado.",
      is_priority=True,
      user_id=reservation.user_id
    )
    
    notification_service.create(db, notification_dto)
  except Exception:
    logger.error(f"Error creando notificación para reserva lista {id}", exc_info=True)

  return get_by_id(db, id)


# -----------------------------------------------------------------
# UPDATE - MARK AS EXPIRED
def mark_as_expired(db: Session, id: int):
  reservation = repository.get_by_id(db, id)
  if not reservation:
    return None

  if int(reservation.reservation_status_id) != 1:
    raise ValueError("Solo se puede marcar como vencida una reserva pendiente")

  repository.update_status(db, id, 4)
  return get_by_id(db, id)


# -----------------------------------------------------------------
# UPDATE - EXPIRE OVERDUE
def expire_overdue_reservations(db: Session) -> int:
  try:
    return repository.expire_overdue_as_expired(db)
  except Exception as e:
    raise e

