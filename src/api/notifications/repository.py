from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from . import models


def get_all(db: Session):
  try:
    return (
      db.query(models.Notification)
      .options(joinedload(models.Notification.user))
      .order_by(models.Notification.created_at.desc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e


def get_by_id(db: Session, id: int):
  try:
    return (
      db.query(models.Notification)
      .options(joinedload(models.Notification.user))
      .filter(models.Notification.id_notification == id)
      .first()
    )
  except SQLAlchemyError as e:
    raise e


def get_by_user_id(db: Session, user_id: str):
  try:
    return (
      db.query(models.Notification)
      .options(joinedload(models.Notification.user))
      .filter(models.Notification.user_id == user_id)
      .order_by(models.Notification.created_at.desc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e


def get_unread_by_user_id(db: Session, user_id: str):
  try:
    return (
      db.query(models.Notification)
      .options(joinedload(models.Notification.user))
      .filter(
        models.Notification.user_id == user_id,
        models.Notification.is_read == False
      )
      .order_by(models.Notification.created_at.desc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e


def create(db: Session, notification: models.Notification):
  try:
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification
  except SQLAlchemyError as e:
    db.rollback()
    raise e


def mark_as_read(db: Session, id: int):
  try:
    notification = db.query(models.Notification).filter(models.Notification.id_notification == id).first()
    if notification:
      notification.is_read = True
      db.commit()
      db.refresh(notification)
    return notification
  except SQLAlchemyError as e:
    db.rollback()
    raise e


def mark_all_as_read(db: Session, user_id: str):
  try:
    result = (
      db.query(models.Notification)
      .filter(
        models.Notification.user_id == user_id,
        models.Notification.is_read == False
      )
      .update({"is_read": True})
    )
    db.commit()
    return result
  except SQLAlchemyError as e:
    db.rollback()
    raise e


def delete(db: Session, id: int):
  try:
    notification = db.query(models.Notification).filter(models.Notification.id_notification == id).first()
    if notification:
      db.delete(notification)
      db.commit()
      return True
    return None
  except SQLAlchemyError as e:
    db.rollback()
    raise e


def delete_by_user(db: Session, user_id: str):
  try:
    result = db.query(models.Notification).filter(models.Notification.user_id == user_id).delete()
    db.commit()
    return result
  except SQLAlchemyError as e:
    db.rollback()
    raise e
