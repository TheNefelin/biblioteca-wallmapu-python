from datetime import datetime, timedelta, date
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from src.schemas.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.schemas.dtos import (
    CreateReservationDTO,
    ReservationDTO,
    ReservationDetailDTO,
)
from src.api.loan_policies import repository as loan_policy_repository
from src.api.loans import repository as loan_repository, service as loan_service, dtos as loan_dtos
from src.api.copy import repository as copy_repository
from src.api.notifications import service as notification_service
from src.api.users import repository as user_repository
from src.models import models
from . import repository

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------
# HELPER - Mapea entidad a DTO con relaciones
def _map_reservation_to_detail(reservation) -> ReservationDetailDTO:
  copy = reservation.copy
  book = copy.edition.book if copy and copy.edition else None

  return ReservationDetailDTO(
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
async def get_all_pagination(db: AsyncSession, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[ReservationDetailDTO]]:
  page = await repository.get_all_pagination(db, pagination)
  return PaginationResponseDTO[list[ReservationDetailDTO]](
    page=page.page,
    pages=page.pages,
    items=page.items,
    data=[_map_reservation_to_detail(r) for r in page.data],
    next=page.next,
    prev=page.prev,
  )


# -----------------------------------------------------------------
# GET USER PAGINATION
async def get_all_pagination_by_user(db: AsyncSession, user_id: UUID, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[ReservationDetailDTO]]:
  page = await repository.get_all_pagination_by_user(db, user_id, pagination)
  return PaginationResponseDTO[list[ReservationDetailDTO]](
    page=page.page,
    pages=page.pages,
    items=page.items,
    data=[_map_reservation_to_detail(r) for r in page.data],
    next=page.next,
    prev=page.prev,
  )


# -----------------------------------------------------------------
# GET BY ID
async def get_by_id(db: AsyncSession, id: int) -> ReservationDetailDTO | None:
  reservation = await repository.get_by_id(db, id)

  if not reservation:
    return None

  return _map_reservation_to_detail(reservation)


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, user_id: UUID, dto: CreateReservationDTO) -> ReservationDTO:
  copy = await copy_repository.get_by_id(db, dto.copy_id)

  if not copy:
    raise ValueError("Ejemplar no encontrado")

  book_id = copy.edition.book_id

  if int(copy.status_id) != 1:
    raise ValueError("El ejemplar no estÃ¡ disponible")

  user_entity = await user_repository.get_by_id_detailed(db, user_id)
  if not user_entity or int(user_entity.user_status_id) != 1:
    raise ValueError("No puedes realizar reservas si tu cuenta no estÃ¡ activa")

  loan_policy = await loan_policy_repository.get_default_policy(db)
  reservation_days = int(loan_policy.reservation_days)
  expiration_date = date.today() + timedelta(days=reservation_days)

  # Obtener reservas y prÃ©stamos activos del usuario
  active_reservations = await repository.get_active_by_user(db, user_id)
  active_loans = await loan_repository.get_active_by_user(db, user_id)

  # 1. Validar lÃ­mite de Loan Policies
  total = len(active_reservations) + len(active_loans)

  if total >= loan_policy.max_books:
    raise ValueError("Has alcanzado el lÃ­mite mÃ¡ximo de reservas y/o prÃ©stamos de libros")

  # 2. Validar que el libro NO estÃ© ya en reservas o prÃ©stamos activos
  book_in_reservations = any(r[2] == book_id for r in active_reservations)
  book_in_loans = any(l[2] == book_id for l in active_loans)

  if book_in_reservations or book_in_loans:
    raise ValueError("Ya tienes este libro reservado o prestado")

  reservation_dto = ReservationDTO(
    user_id=user_id,
    copy_id=dto.copy_id,
    expiration_date=expiration_date
  )

  # Crear Reserva
  created = await repository.create(db, reservation_dto.model_dump(exclude_none=True))

  if not created or not created.id_reservation:
    raise ValueError("Error al crear la reserva")

  # Disparar notificaciÃ³n (efecto secundario resiliente)
  await notification_service.notification_for_create_reservation_and_send_email(db, created.id_reservation)

  return ReservationDTO.model_validate(created)


# -----------------------------------------------------------------
# UPDATE - CANCEL
async def mark_as_cancelled(db: AsyncSession, id: int) -> ReservationDTO:
  reservation = await repository.get_by_id(db, id)

  if not reservation:
    return None

  if int(reservation.reservation_status_id) != 1:
    raise ValueError("Solo se puede cancelar una reserva pendiente")

  # Actualiza Reserva
  updated = await repository.update_status(db, id, 3)

  # Disparar notificaciÃ³n (efecto secundario resiliente)
  await notification_service.notification_for_cancel_reservation_and_send_email(db, updated.id_reservation)

  return ReservationDTO.model_validate(updated)


# -----------------------------------------------------------------
# UPDATE - MARK AS PICKUP AND CREATE LOAN
async def mark_as_pickup(db: AsyncSession, id: int, copy_id: int) -> ReservationDTO:
  reservation = await repository.get_by_id(db, id)
  if not reservation:
    return None

  if int(reservation.reservation_status_id) != 1:
    raise ValueError("Solo se puede marcar como retirada una reserva pendiente")

  if reservation.expiration_date < datetime.now():
    raise ValueError("No se puede entregar una reserva vencida. Debe generar una nueva.")

  copy = await copy_repository.get_by_id(db, copy_id)
  if not copy:
    raise ValueError("Ejemplar no encontrado")

  if int(copy.status_id) != 1:
    raise ValueError("El ejemplar no estÃ¡ disponible")

  loan_dto = loan_dtos.CreateLoanDTO(
    copy_id=copy.id_copy,
    user_id=reservation.user_id,
  )

  await loan_service.create(db, loan_dto)
  updated_reservation = await repository.update_status(db, id, 2)

  return ReservationDTO.model_validate(updated_reservation)


# -----------------------------------------------------------------
# UPDATE - MARK AS EXPIRED
async def mark_as_expired(db: AsyncSession, id: int) -> ReservationDTO:
  reservation = await repository.get_by_id(db, id)
  if not reservation:
    return None

  if int(reservation.reservation_status_id) != 1:
    raise ValueError("Solo se puede marcar como vencida una reserva pendiente")

  updated = await repository.update_status(db, id, 4)

  return ReservationDTO.model_validate(updated)


# -----------------------------------------------------------------
# UPDATE - EXPIRE OVERDUE
async def expire_overdue_reservations(db: AsyncSession) -> int:
  return await repository.bulk_update_status_by_expired(db, old_status_id=1, new_status_id=4)