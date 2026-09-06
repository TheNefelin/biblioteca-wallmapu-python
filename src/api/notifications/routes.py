from uuid import UUID
from fastapi import APIRouter, Depends, Query, Request, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.api.users import service as user_service
from src.core.database import get_db_async
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.core.exceptions import NotFoundError
from src.schemas.dtos import PaginationRequest, PaginationResponse
from src.schemas.dtos import (
  NotificationByEmailRequest,
  NotificationResponse,
  NotificationDetailResponse,
  NotificationFilterRequest,
)
from . import service
from .connection_manager import manager

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))
user_required = Depends(get_current_user(required_roles=[UserRole.LECTOR]))
user_or_admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(
  prefix="/notifications",
  tags=["notifications"],
)


# -----------------------------------------------------------------
# ADMIN: GET ALL PAGINATED
@router.get(
  "/pagination",
  response_model=PaginationResponse[list[NotificationDetailResponse]],
  status_code=HTTP_200_OK,
  summary="Listar todas las notificaciones con paginación",
  description="Retorna lista paginada de notificaciones. Admin ve todas. Filtros: search (título/mensaje)",
  dependencies=[admin_required],
)
async def get_all_notifications_paginated(
  request: Request,
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  is_read: bool = Query(default=True, description="true=todos, false=solo no leídas"),
  db: AsyncSession = Depends(get_db_async)
):
  filter = NotificationFilterRequest(is_read=is_read)

  pagination_request = PaginationRequest[NotificationFilterRequest](
    page=page,
    limit=limit,
    search=search or "",
    filter=filter,
  )

  pagination_response = await service.get_all_pagination(db, pagination_request)

  if pagination_response.pages > pagination_response.page:
    pagination_response.next = str(request.url.include_query_params(page=pagination_response.page + 1, limit=limit))
  if pagination_response.page > 1:
    pagination_response.prev = str(request.url.include_query_params(page=pagination_response.page - 1, limit=limit))

  return pagination_response

# -----------------------------------------------------------------
# USER: GET USER NOTIFICATIONS PAGINATED
@router.get(
  "/user/pagination",
  response_model=PaginationResponse[list[NotificationDetailResponse]],
  status_code=HTTP_200_OK,
  summary="Mis notificaciones paginadas",
  description="Retorna notificaciones del usuario actual (extraído del token JWT). Filtros: search",
  dependencies=[user_or_admin_required],
)
async def get_user_notifications(
  request: Request,
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  is_read: bool = Query(default=True, description="true=todos, false=solo no leídas"),
  current_user: dict = Depends(get_current_user()),
  db: AsyncSession = Depends(get_db_async),
):
  user_id = UUID(current_user["sub"])

  filter = NotificationFilterRequest(is_read=is_read)

  pagination_request = PaginationRequest[NotificationFilterRequest](
    page=page,
    limit=limit,
    search=search or "",
    filter=filter,
  )

  pagination_response = await service.get_by_user_paginated(db, user_id, pagination_request)

  if pagination_response.pages > pagination_response.page:
    pagination_response.next = str(request.url.include_query_params(page=pagination_response.page + 1, limit=limit))
  if pagination_response.page > 1:
    pagination_response.prev = str(request.url.include_query_params(page=pagination_response.page - 1, limit=limit))

  return pagination_response

# -----------------------------------------------------------------
# USER: GET UNREAD COUNT (For badge)
@router.get(
  "/user/unread-count",
  response_model=int,
  status_code=HTTP_200_OK,
  summary="Contar notificaciones no leídas",
  description="Retorna la cantidad de notificaciones no leídas del usuario (para badge en header)",
  dependencies=[user_or_admin_required],
)
async def get_unread_count(
  current_user: dict = Depends(get_current_user()),
  db: AsyncSession = Depends(get_db_async)
):
  user_id = UUID(current_user["sub"])

  count = await service.count_unread_by_user_id(db, user_id)
  return count

# -----------------------------------------------------------------
# GET BY ID
@router.get(
  "/{id}",
  response_model=NotificationResponse,
  status_code=HTTP_200_OK,
  summary="Obtener notificación por ID",
  description="Retorna una notificación específica por su ID",
  dependencies=[user_required],
)
async def get_notification_by_id(
  id: int,
  db: AsyncSession = Depends(get_db_async)
):
  res = await service.get_by_id(db, id)
  if not res:
    raise NotFoundError(entity="Notificación")
  return res

# -----------------------------------------------------------------
# ADMIN: CREATE NOTIFICATION
@router.post(
  "",
  response_model=NotificationResponse,
  status_code=HTTP_201_CREATED,
  summary="Crear notificación",
  description="Crea una nueva notificación para un usuario específico. Usado para anuncios generales de la biblioteca",
  dependencies=[admin_required]
)
async def create_notification(
  dto: NotificationByEmailRequest,
  db: AsyncSession = Depends(get_db_async)
):
  user = await user_service.get_by_email(db, dto.email)
  if not user:
    raise NotFoundError(entity="Usuario")

  res = await service.create(db, dto, user.id_user)
  return res

# -----------------------------------------------------------------
# USER: MARK AS READ
@router.put(
  "/user/{id}/read",
  response_model=bool,
  status_code=HTTP_200_OK,
  summary="Marcar notificación como leída",
  description="Marca una notificación específica como leída. Verifica que pertenezca al usuario del token",
  dependencies=[user_or_admin_required]
)
async def mark_notification_as_read(
  id: int,
  current_user: dict = Depends(get_current_user()),
  db: AsyncSession = Depends(get_db_async)
):
  user_id = UUID(current_user["sub"])

  success = await service.mark_as_read(db, id, str(user_id))

  if not success:
    raise NotFoundError(entity="Notificación")

  return True

# -----------------------------------------------------------------
# USER: MARK ALL AS READ
@router.put(
  "/user/read-all",
  response_model=bool,
  status_code=HTTP_200_OK,
  summary="Marcar todas como leídas",
  description="Marca todas las notificaciones del usuario actual como leídas",
  dependencies=[user_or_admin_required]
)
async def mark_all_notifications_as_read(
  current_user: dict = Depends(get_current_user()),
  db: AsyncSession = Depends(get_db_async)
):
  user_id = UUID(current_user["sub"])

  success = await service.mark_all_as_read(db, str(user_id))

  return success

# -----------------------------------------------------------------
# WEBSOCKET: Tiempo real para notificaciones
@router.websocket("/ws")
async def websocket_endpoint(
  websocket: WebSocket,
  token: str = None
):
  # Validar token JWT (extraer user_id)
  try:
    from src.core.security import verify_token
    payload = verify_token(token)
    user_id = payload.get("sub")

    if not user_id:
      await websocket.close(code=4000, reason="Invalid token")
      return

    await manager.connect(websocket, user_id)

    # Enviar count inicial
    # Nota: En producción, usa una sesión de BD apropiada
    # Por simplicidad, omitimos el count inicial

    try:
      while True:
        # Recibir mensajes del cliente (opcional)
        data = await websocket.receive_text()
    except WebSocketDisconnect:
      manager.disconnect(websocket, user_id)
  except Exception as e:
    await websocket.close(code=4000, reason=str(e))