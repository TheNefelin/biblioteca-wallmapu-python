from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))
user_required = Depends(get_current_user(required_roles=[UserRole.LECTOR]))
user_or_admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(
  prefix="/notifications",
  tags=["notifications"],
)


#@router.get(
#  "/TRY",
#  response_model=ApiResponse[list[dtos.NotificationDTO]],
#  status_code=HTTP_200_OK,
#)
#def get_try(
#  db: Session = Depends(get_db)
#):
#  try:
#    res = service.notification_for_return_loan_and_send_email(db, 10021)
#    return ApiResponse.success(data=res)
#  except Exception as e:
#    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# ADMIN: GET ALL PAGINATED
@router.get(
  "/pagination",
  response_model=ApiResponse[PaginationResponseDTO[list[dtos.NotificationDetailDTO]]],
  status_code=HTTP_200_OK,
  summary="Listar todas las notificaciones con paginación",
  description="Retorna lista paginada de notificaciones. Admin ve todas. Filtros: search (título/mensaje)",
  #dependencies=[admin_required],
)
def get_all_notifications_paginated(
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  db: Session = Depends(get_db)
):
  try:
    pagination_request = PaginationRequestDTO[None](
      page=page,
      limit=limit,
      search=search or "",
      filter=None,
    )

    pagination_response = service.get_all_paginated(db, pagination_request)
    return ApiResponse.success(data=pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# USER: GET USER NOTIFICATIONS PAGINATED
@router.get(
  "/user/pagination",
  response_model=ApiResponse[PaginationResponseDTO[list[dtos.NotificationDetailDTO]]],
  status_code=HTTP_200_OK,
  summary="Mis notificaciones paginadas",
  description="Retorna notificaciones del usuario actual (extraído del token JWT). Filtros: search",
  dependencies=[user_required],
)
def get_user_notifications(
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  current_user = Depends(get_current_user()),
  db: Session = Depends(get_db),
):
  try:
    user_id = UUID(current_user["sub"])

    pagination_request = PaginationRequestDTO[None](
      page=page,
      limit=limit,
      search=search or "",
      filter=None,
    )

    pagination_response = service.get_by_user_paginated(db, user_id, pagination_request)
    return ApiResponse.success(data=pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# USER: GET UNREAD COUNT (For badge)
@router.get(
  "/user/unread-count",
  response_model=ApiResponse[int],
  status_code=HTTP_200_OK,
  summary="Contar notificaciones no leídas",
  description="Retorna la cantidad de notificaciones no leídas del usuario (para badge en header)",
  dependencies=[user_required],
)
def get_unread_count(
  current_user = Depends(get_current_user()),
  db: Session = Depends(get_db)
):
  try:
    user_id = UUID(current_user["sub"])
    
    count = service.count_unread_by_user_id(db, user_id)
    return ApiResponse.success(data=count)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# USER: GET UNREAD LIST
@router.get(
  "/user/unread",
  response_model=ApiResponse[list[dtos.NotificationDTO]],
  status_code=HTTP_200_OK,
  summary="Listar notificaciones no leídas",
  description="Retorna lista de notificaciones no leídas del usuario actual",
  dependencies=[user_required],
)
def get_unread_notifications(
  current_user = Depends(get_current_user()),
  db: Session = Depends(get_db)
):
  try:
    user_id = UUID(current_user["sub"])

    res = service.get_unread_by_user_id(db, user_id)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET BY ID
@router.get(
  "/{id}",
  response_model=ApiResponse[dtos.NotificationDTO],
  status_code=HTTP_200_OK,
  summary="Obtener notificación por ID",
  description="Retorna una notificación específica por su ID",
  dependencies=[user_required],
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


# -----------------------------------------------------------------
# ADMIN: CREATE NOTIFICATION
@router.post(
  "",
  response_model=ApiResponse[dtos.NotificationDTO],
  status_code=HTTP_201_CREATED,
  summary="Crear notificación (Admin)",
  description="Crea una nueva notificación para un usuario específico. Usado para anuncios generales de la biblioteca",
  #dependencies=[admin_required]
)
def create_notification(
  dto: dtos.CreateNotificationByEmailDTO,
  db: Session = Depends(get_db)
):
  try:
    res = service.create(db, dto)
    return ApiResponse.created(data=res, message="Notificación creada")
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# USER: MARK AS READ
@router.put(
  "/user/{id}/read",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  summary="Marcar notificación como leída",
  description="Marca una notificación específica como leída. Verifica que pertenezca al usuario del token",
  dependencies=[user_required]
)
def mark_notification_as_read(
  id: int,
  current_user = Depends(get_current_user()),
  db: Session = Depends(get_db)
):
  try:
    user_id = UUID(current_user["sub"])

    success = service.mark_as_read(db, id, str(user_id))
    if not success:
      return ApiResponse.not_found(message="Notificación no encontrada o no pertenece al usuario")
    return ApiResponse.success(data=True, message="Notificación marcada como leída")
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# USER: MARK ALL AS READ
@router.put(
  "/user/read-all",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  summary="Marcar todas como leídas",
  description="Marca todas las notificaciones del usuario actual como leídas",
  dependencies=[user_required]
)
def mark_all_notifications_as_read(
  current_user = Depends(get_current_user()),
  db: Session = Depends(get_db)
):
  try:
    user_id = UUID(current_user["sub"])

    success = service.mark_all_as_read(db, str(user_id))
    return ApiResponse.success(data=success, message=f"Notificaciones marcadas como leídas")
  except Exception as e:
    return ApiResponse.server_error(str(e))



