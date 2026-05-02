from sqlalchemy.orm import Session
from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.services.email_service import (
  send_reservation_created_email,
  send_reservation_cancelled_email,
  send_reservation_ready_email
)
from . import dtos, repository, models


# -----------------------------------------------------------------
# GET ALL PAGINATED (Admin)
def get_all_paginated(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.NotificationDTO]]:
  pagination_response = repository.get_all_paginated(db, pagination)
  items = pagination_response.data or []

  data = [dtos.NotificationDTO.model_validate(item) for item in items]

  return PaginationResponseDTO[list[dtos.NotificationDTO]](
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
    next=pagination_response.next,
    prev=pagination_response.prev,
  )


# -----------------------------------------------------------------
# GET BY USER PAGINATED
def get_by_user_paginated(db: Session, user_id: str, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.NotificationDTO]]:
  pagination_response = repository.get_by_user_paginated(db, user_id, pagination)
  items = pagination_response.data or []

  data = [dtos.NotificationDTO.model_validate(item) for item in items]

  return PaginationResponseDTO[list[dtos.NotificationDTO]](
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
    next=pagination_response.next,
    prev=pagination_response.prev,
  )


# -----------------------------------------------------------------
# COUNT UNREAD BY USER (For badge)
def count_unread_by_user_id(db: Session, user_id: str) -> int:
  return repository.count_unread_by_user_id(db, user_id)


# -----------------------------------------------------------------
# GET UNREAD BY USER (List)
def get_unread_by_user_id(db: Session, user_id: str):
  notifications = repository.get_unread_by_user_id(db, user_id)
  return  [dtos.NotificationDTO.model_validate(item) for item in notifications]


# -----------------------------------------------------------------
# GET BY ID
def get_by_id(db: Session, id: int):
  notification = repository.get_by_id(db, id)
  
  if not notification:
    return None

  return dtos.NotificationDTO.model_validate(notification)


# -----------------------------------------------------------------
# CREATE
def create(db: Session, dto: dtos.CreateNotificationDTO):
  try:
    created = repository.create(db, dto.model_dump(exclude_unset=True))

    if not created or not created.id_notification:
      raise ValueError("Error al crear la Notificacion")

    # Disparar email (efecto secundario resiliente)
    try:
      user_email = created.user.email if created.user else None
      if user_email:
        _send_email_by_title(
          title=created.title,
          user_email=user_email,
          message=created.message
        )
    except Exception:
      # Log opcional: no interrumpe la notificación si falla el email
      print(f"Error al enviar el email: {e}")
      pass

    return dtos.NotificationDTO.model_validate(created)
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# HELPER - Send email based on notification title
def _send_email_by_title(title: str, user_email: str, message: str):
  """
  Dispatch email sending based on notification title.
  Extracts reservation_id from message to pass to email functions.
  """
  # Mapping: notification title -> (email_function, extra_args)
  email_mapping = {
    "RESERVA CREADA": (
      send_reservation_created_email,
      {"book_title": _extract_book_title(message), "expiration_date": _extract_expiration_date(message)}
    ),
    "RESERVA CANCELADA": (
      send_reservation_cancelled_email,
      {"book_title": _extract_book_title(message)}
    ),
    "RESERVA LISTA": (
      send_reservation_ready_email,
      {"book_title": _extract_book_title(message)}
    ),
  }

  if title in email_mapping:
    email_func, extra_args = email_mapping[title]
    # Extract reservation_id from message (e.g., "Reserva #123 registrada")
    reservation_id = _extract_reservation_id(message)
    if reservation_id > 0:
      email_func(
        to_email=user_email,
        reservation_id=reservation_id,
        **extra_args
      )


# -----------------------------------------------------------------
# HELPERS - Extract data from notification message
def _extract_reservation_id(message: str) -> int:
  """Extract reservation ID from notification message like 'Reserva #123 registrada'."""
  import re
  match = re.search(r'Reserva #(\d+)', message)
  if match:
    return int(match.group(1))
  return 0


def _extract_book_title(message: str) -> str:
  """Extract book title from notification message."""
  if "Ejemplar:" in message:
    parts = message.split("Ejemplar:")
    if len(parts) > 1:
      return parts[1].split(".")[0].strip()
  return "Libro"


def _extract_expiration_date(message: str) -> str:
  """Extract expiration date from notification message."""
  if "Vence:" in message:
    parts = message.split("Vence:")
    if len(parts) > 1:
      return parts[1].strip()
  return ""


# -----------------------------------------------------------------
# MARK AS READ
def mark_as_read(db: Session, id: int):
  notification = repository.mark_as_read(db, id)
  if not notification:
    return None
  return get_by_id(db, id)


# -----------------------------------------------------------------
# MARK ALL AS READ
def mark_all_as_read(db: Session, user_id: str):
  return repository.mark_all_as_read(db, user_id)


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, id: int):
  return repository.delete(db, id)


def _to_dto(notification: models.Notification) -> dtos.NotificationDTO:
  return dtos.NotificationDTO(
    id_notification=notification.id_notification,
    title=notification.title,
    message=notification.message,
    is_priority=notification.is_priority,
    is_read=notification.is_read,
    user_id=notification.user_id,
    user_name=notification.user.name if notification.user else None,
    user_email=notification.user.email if notification.user else None,
    created_at=notification.created_at
  )
