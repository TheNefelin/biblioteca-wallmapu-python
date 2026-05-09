from sqlalchemy.orm import Session
import logging

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.api.reservations import repository as reservation_repository
from src.api.loans import repository as loan_repository
from src.api.users import repository as user_repository
from src.services import email_service
from . import dtos, repository

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------
# GET ALL PAGINATED (Admin)
def get_all_paginated(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.NotificationDetailDTO]]:
  pagination_response = repository.get_all_paginated(db, pagination)
  items = pagination_response.data or []

  data = [dtos.NotificationDetailDTO(
    **dtos.NotificationDTO.model_validate(item).model_dump(),
    email=item.user.email if item.user else ""
  ) for item in items]

  return PaginationResponseDTO[list[dtos.NotificationDetailDTO]](
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
    next=pagination_response.next,
    prev=pagination_response.prev,
  )


# -----------------------------------------------------------------
# GET BY USER PAGINATED
def get_by_user_paginated(db: Session, user_id: str, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.NotificationDetailDTO]]:
  pagination_response = repository.get_by_user_paginated(db, user_id, pagination)
  items = pagination_response.data or []

  data = [dtos.NotificationDetailDTO(
    **dtos.NotificationDTO.model_validate(item).model_dump(),
    email=item.user.email if item.user else ""
  ) for item in items]

  return PaginationResponseDTO[list[dtos.NotificationDetailDTO]](
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
# GET BY ID
def get_by_id(db: Session, id: int) -> dtos.NotificationDTO | None:
  notification = repository.get_by_id(db, id)
  if not notification:
    return None
  return dtos.NotificationDTO.model_validate(notification)


# -----------------------------------------------------------------
# CREATE
def create(db: Session, dto: dtos.CreateNotificationByEmailDTO) -> dtos.NotificationDTO | None:
  user = user_repository.get_by_email(db, dto.email)

  if not user:
    raise ValueError("El Usuario no Existe en la Base de Datos")

  email_data = email_service.AdminEmailData(
    title=dto.title,
    message=dto.message,
    is_priority=dto.is_priority,
    user_email=dto.email,
  )

  notification = dtos.CreateNotificationDTO(
    title=dto.title,
    message=dto.message,
    is_priority=dto.is_priority,
    user_id=user.id_user
  )

  created = repository.create(db, notification.model_dump(exclude_unset=True))

  if not created or not created.id_notification:
    raise ValueError("Error al crear la Notificacion")

  try:
    response = email_service.send_admin_email(data=email_data)

    if not response or response.get("messageId") is None:
      logger.warning(f"Email no fue enviado correctamente para notification {created.id_notification}")
  except Exception:
    print(f"Error al enviar el email: {created.id_notification}")
    logger.error(f"Error al enviar el email: {created.id_notification}", exc_info=True)

  return dtos.NotificationDTO.model_validate(created)


# -----------------------------------------------------------------
# CREATE WELCOME NOTIFICATION
def create_welcome_notification(db: Session, user_id: str, user_email: str, user_name: str):
  notification = dtos.CreateNotificationDTO(
    title="BIENVENIDO/A",
    message=f"¡Bienvenido/a {user_name}! Tu cuenta ha sido creada exitosamente en Biblioteca Wallmapu.",
    is_priority=False,
    user_id=user_id
  )
  created = repository.create(db, notification.model_dump(exclude_unset=True))

  if not created or not created.id_notification:
    logger.warning(f"Error al crear notificación de bienvenida para user {user_id}")
    return

  try:
    email_data = email_service.WelcomeEmailData(user_email=user_email, user_name=user_name)
    email_service.send_welcome_email(data=email_data)
  except Exception:
    logger.error(f"Error al enviar email de bienvenida para user {user_id}", exc_info=True)


# -----------------------------------------------------------------
# CREATE NOTIFICATION FOR RESERVATION
def notification_for_create_reservation_and_send_email(db: Session, reservation_id: int):
  reservation = reservation_repository.get_by_id(db, reservation_id)

  email_data = email_service.EmailData(
    id=reservation.id_reservation,
    book_title=reservation.copy.edition.book.title,
    book_barcode=reservation.copy.barcode,
    user_email=reservation.user.email,
    expiration_date=reservation.expiration_date
  )

  notification = dtos.CreateNotificationDTO(
    title="RESERVA CREADA",
    message=f"Reserva #{email_data.id} registrada. Ejemplar: {email_data.book_title}. CodBarra: {email_data.book_barcode}. Vence: {email_data.expiration_date.strftime('%d-%m-%Y')}",
    is_priority=False,
    user_id=reservation.user_id
  )

  created = repository.create(db, notification.model_dump(exclude_unset=True))

  if not created or not created.id_notification:
    raise ValueError("Error al crear la Notificacion")

  try:
    email_service.send_reservation_created_email(data=email_data)
  except Exception:
    print(f"Error al enviar el email: {created.id_notification}")
    logger.error(f"Error al enviar el email: {created.id_notification}", exc_info=True)


# -----------------------------------------------------------------
# CREATE NOTIFICATION FOR CANCEL RESERVATION
def notification_for_cancel_reservation_and_send_email(db: Session, reservation_id: int):
  reservation = reservation_repository.get_by_id(db, reservation_id)

  email_data = email_service.EmailData(
    id=reservation.id_reservation,
    book_title=reservation.copy.edition.book.title,
    book_barcode=reservation.copy.barcode,
    user_email=reservation.user.email,
  )

  notification = dtos.CreateNotificationDTO(
    title="RESERVA CANCELADA",
    message=f"Reserva #{email_data.id} cancelada. Ejemplar: {email_data.book_title}. CodBarra: {email_data.book_barcode}.",
    is_priority=False,
    user_id=reservation.user_id
  )

  created = repository.create(db, notification.model_dump(exclude_unset=True))

  if not created or not created.id_notification:
    raise ValueError("Error al crear la Notificacion")

  try:
    email_service.send_reservation_cancelled_email(data=email_data)
  except Exception:
    print(f"Error creando notificación para reserva cancelada {reservation_id}")
    logger.error(f"Error creando notificación para reserva cancelada {reservation_id}", exc_info=True)


# -----------------------------------------------------------------
# CREATE NOTIFICATION FOR CREATE LOAN
def notification_for_create_loan_and_send_email(db: Session, loan_id: int):
  loan = loan_repository.get_by_id(db, loan_id)

  email_data = email_service.EmailData(
    id=loan.id_loan,
    book_title=loan.copy.edition.book.title,
    book_barcode=loan.copy.barcode,
    user_email=loan.user.email,
    expiration_date=loan.due_date,
  )

  notification = dtos.CreateNotificationDTO(
    title="PRÉSTAMO REALIZADO",
    message=f"Préstamo #{email_data.id} registrado. Ejemplar: {email_data.book_title}. CodBarra: {email_data.book_barcode}. Vence: {email_data.expiration_date.strftime('%d-%m-%Y')}",
    is_priority=False,
    user_id=loan.user_id
  )

  created = repository.create(db, notification.model_dump(exclude_unset=True))

  if not created or not created.id_notification:
    raise ValueError("Error al crear la Notificacion")

  try:
    email_service.send_loan_created_email(data=email_data)
  except Exception:
    print(f"Error al enviar el email: {created.id_notification}")
    logger.error(f"Error al enviar el email: {created.id_notification}", exc_info=True)


# -----------------------------------------------------------------
# CREATE NOTIFICATION FOR RETURN LOAN
def notification_for_return_loan_and_send_email(db: Session, loan_id: int):
  loan = loan_repository.get_by_id(db, loan_id)

  email_data = email_service.EmailData(
    id=loan.id_loan,
    book_title=loan.copy.edition.book.title,
    book_barcode=loan.copy.barcode,
    user_email=loan.user.email,
  )

  notification = dtos.CreateNotificationDTO(
    title="PRÉSTAMO DEVUELTO",
    message=f"Préstamo #{loan.id_loan} devuelto exitosamente.",
    is_priority=False,
    user_id=loan.user_id
  )

  created = repository.create(db, notification.model_dump(exclude_unset=True))

  if not created or not created.id_notification:
    raise ValueError("Error al crear la Notificacion")

  try:
    email_service.send_loan_returned_email(data=email_data)
  except Exception:
    print(f"Error al enviar el email: {created.id_notification}")
    logger.error(f"Error al enviar el email: {created.id_notification}", exc_info=True)


# -----------------------------------------------------------------
# MARK AS READ
def mark_as_read(db: Session, id: int, user_id: str) -> bool:
  notification = repository.get_by_id(db, id)
  if not notification:
    return False
    
  # Validar que la notificación pertenezca al usuario
  if str(notification.user_id) != str(user_id):
    return False
    
  repository.mark_as_read(db, id)
  return True


# -----------------------------------------------------------------
# MARK ALL AS READ
def mark_all_as_read(db: Session, user_id: str) -> bool:
  result = repository.mark_all_as_read(db, user_id)
  return result > 0
