from sqlalchemy.orm import Session
from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
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

    return dtos.NotificationDTO.model_validate(created)
  except Exception as e:
    raise e


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
