from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))
user_or_admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(
  prefix="/notifications",
  tags=["notifications"],
)


@router.get(
  "/",
  response_model=ApiResponse[List[dtos.NotificationDetailDTO]],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def get_all_notifications(db: Session = Depends(get_db)):
  try:
    res = service.get_all(db)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.get(
  "/user/{user_id}",
  response_model=ApiResponse[List[dtos.NotificationDetailDTO]],
  status_code=HTTP_200_OK,
  dependencies=[user_or_admin_required]
)
def get_notifications_by_user(
  user_id: str,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_by_user_id(db, user_id)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.get(
  "/user/{user_id}/unread",
  response_model=ApiResponse[List[dtos.NotificationDetailDTO]],
  status_code=HTTP_200_OK,
  dependencies=[user_or_admin_required]
)
def get_unread_notifications(
  user_id: str,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_unread_by_user_id(db, user_id)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.get(
  "/{id}",
  response_model=ApiResponse[dtos.NotificationDetailDTO],
  status_code=HTTP_200_OK
)
def get_notification_by_id(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_by_id(db, id)
    if not res:
      return ApiResponse.not_found(message="Notificación no encontrada")
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.post(
  "/",
  response_model=ApiResponse[dtos.NotificationDetailDTO],
  status_code=HTTP_201_CREATED,
  dependencies=[admin_required]
)
def create_notification(
  dto: dtos.CreateNotificationDTO,
  db: Session = Depends(get_db)
):
  try:
    res = service.create(db, dto)
    return ApiResponse.created(data=res, message="Notificación creada")
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.put(
  "/{id}/read",
  response_model=ApiResponse[dtos.NotificationDetailDTO],
  status_code=HTTP_200_OK,
  dependencies=[user_or_admin_required]
)
def mark_notification_as_read(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.mark_as_read(db, id)
    if not res:
      return ApiResponse.not_found(message="Notificación no encontrada")
    return ApiResponse.success(data=res, message="Notificación marcada como leída")
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.put(
  "/user/{user_id}/read-all",
  response_model=ApiResponse[int],
  status_code=HTTP_200_OK,
  dependencies=[user_or_admin_required]
)
def mark_all_notifications_as_read(
  user_id: str,
  db: Session = Depends(get_db)
):
  try:
    count = service.mark_all_as_read(db, user_id)
    return ApiResponse.success(data=count, message=f"{count} notificaciones marcadas como leídas")
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.delete(
  "/{id}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def delete_notification(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.delete(db, id)
    if res is None:
      return ApiResponse.not_found(message="Notificación no encontrada")
    return ApiResponse.success(data=res, message="Notificación eliminada")
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.delete(
  "/user/{user_id}",
  response_model=ApiResponse[int],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def delete_notifications_by_user(
  user_id: str,
  db: Session = Depends(get_db)
):
  try:
    count = service.delete_by_user(db, user_id)
    return ApiResponse.success(data=count, message=f"{count} notificaciones eliminadas")
  except Exception as e:
    return ApiResponse.server_error(str(e))
