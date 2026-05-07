from math import ceil
from sqlalchemy.orm import Session, joinedload
from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models


# -----------------------------------------------------------------
# GET ALL PAGINATED (Admin)
def get_all_paginated(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  query = (
    db.query(models.Notification)
    .options(
      joinedload(models.Notification.user)
    )
  )

  is_read_filter = pagination.filter.is_read if pagination.filter else True
  if not is_read_filter:
    query = query.filter(
      models.Notification.is_read == is_read_filter
    )

  search_filter = pagination.search if pagination.search else None
  if search_filter:
    query = query.filter(
      models.Notification.title.ilike(f"%{search_filter}%") |
      models.Notification.message.ilike(f"%{search_filter}%")
    )

  total_items = query.count()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0

  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (
    query
    .order_by(models.Notification.created_at.desc())
    .offset(offset)
    .limit(pagination.limit)
    .all()
  )

  next_url = f"/api/notifications?page={page + 1}&limit={pagination.limit}" if page < total_pages else None
  prev_url = f"/api/notifications?page={page - 1}&limit={pagination.limit}" if page > 1 else None

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=result,
    next=next_url,
    prev=prev_url
  )


# -----------------------------------------------------------------
# GET BY USER PAGINATED
def get_by_user_paginated(db: Session, user_id: str, pagination: PaginationRequestDTO) -> PaginationResponseDTO:
  query = (
    db.query(models.Notification)
    .options(joinedload(models.Notification.user))
    .filter(models.Notification.user_id == user_id)
  )

  is_read_filter = pagination.filter.is_read if pagination.filter else True
  if not is_read_filter:
    query = query.filter(models.Notification.is_read == is_read_filter)

  search_filter = pagination.search if pagination.search else None
  if search_filter:
    query = query.filter(
      models.Notification.title.ilike(f"%{search_filter}%") |
      models.Notification.message.ilike(f"%{search_filter}%")
    )

  total_items = query.count()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0

  page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (page - 1) * pagination.limit

  result = (
    query
    .order_by(models.Notification.created_at.desc())
    .offset(offset)
    .limit(pagination.limit)
    .all()
  )

  next_url = f"/api/notifications/user?page={page + 1}&limit={pagination.limit}" if page < total_pages else None
  prev_url = f"/api/notifications/user?page={page - 1}&limit={pagination.limit}" if page > 1 else None

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=result,
    next=next_url,
    prev=prev_url
  )


# -----------------------------------------------------------------
# GET BY ID
def get_by_id(db: Session, id: int):
  return (
    db.query(models.Notification)
    .options(joinedload(models.Notification.user))
    .filter(models.Notification.id_notification == id)
    .first()
  )


# -----------------------------------------------------------------
# GET UNREAD BY USER (List)
def get_unread_by_user_id(db: Session, user_id: str):
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


# -----------------------------------------------------------------
# COUNT UNREAD BY USER (For badge)
def count_unread_by_user_id(db: Session, user_id: str) -> int:
  return (
    db.query(models.Notification)
    .filter(
      models.Notification.user_id == user_id,
      models.Notification.is_read == False
    )
    .count()
  )


# -----------------------------------------------------------------
# CREATE
def create(db: Session, data: dict) -> models.Notification | None:
  item = models.Notification(**data)
  db.add(item)
  db.commit()
  db.refresh(item)

  return item


# -----------------------------------------------------------------
# MARK AS READ
def mark_as_read(db: Session, id: int):
  notification = db.query(models.Notification).filter(models.Notification.id_notification == id).first()
  if notification:
    notification.is_read = True
    db.commit()
    db.refresh(notification)
  return notification


# -----------------------------------------------------------------
# MARK ALL AS READ
def mark_all_as_read(db: Session, user_id: str):
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


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, id: int):
  notification = db.query(models.Notification).filter(models.Notification.id_notification == id).first()
  if notification:
    db.delete(notification)
    db.commit()
    return True
  return None
