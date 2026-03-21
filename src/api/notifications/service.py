from sqlalchemy.orm import Session
from . import dtos, repository, models


def get_all(db: Session):
  notifications = repository.get_all(db)
  return [_to_detail_dto(n) for n in notifications]


def get_by_id(db: Session, id: int):
  notification = repository.get_by_id(db, id)
  if not notification:
    return None
  return _to_detail_dto(notification)


def get_by_user_id(db: Session, user_id: str):
  notifications = repository.get_by_user_id(db, user_id)
  return [_to_detail_dto(n) for n in notifications]


def get_unread_by_user_id(db: Session, user_id: str):
  notifications = repository.get_unread_by_user_id(db, user_id)
  return [_to_detail_dto(n) for n in notifications]


def create(db: Session, dto: dtos.CreateNotificationDTO):
  notification = models.Notification(
    title=dto.title,
    message=dto.message,
    user_id=dto.user_id,
    is_read=False
  )
  created = repository.create(db, notification)
  return get_by_id(db, created.id_notification)


def mark_as_read(db: Session, id: int):
  notification = repository.mark_as_read(db, id)
  if not notification:
    return None
  return get_by_id(db, id)


def mark_all_as_read(db: Session, user_id: str):
  return repository.mark_all_as_read(db, user_id)


def delete(db: Session, id: int):
  return repository.delete(db, id)


def delete_by_user(db: Session, user_id: str):
  return repository.delete_by_user(db, user_id)


def _to_detail_dto(notification: models.Notification):
  return dtos.NotificationDetailDTO(
    id_notification=notification.id_notification,
    title=notification.title,
    message=notification.message,
    is_read=notification.is_read,
    user_id=notification.user_id,
    user_name=notification.user.name if notification.user else None,
    user_email=notification.user.email if notification.user else None,
    created_at=notification.created_at
  )
