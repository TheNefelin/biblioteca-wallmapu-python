from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db_async
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.core.exceptions import NotFoundError, ForbiddenError, AppError
from src.schemas.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.schemas.dtos import (
    CreateReservationDTO,
    ReservationDTO,
    ReservationDetailDTO,
    ReservationFilterDTO,
    ReservationPickupDTO,
)
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))
user_required = Depends(get_current_user(required_roles=[UserRole.LECTOR]))
user_or_admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(
  prefix="/reservations",
  tags=["reservations"],
)


# -----------------------------------------------------------------
# GET ALL PAGINATION
@router.get(
  "/pagination",
  response_model=PaginationResponseDTO[List[ReservationDetailDTO]],
  status_code=HTTP_200_OK,
  summary="Listar todas las reservas con paginación",
  description="Retorna lista paginada de reservas. Filtros: id_status (1=pendiente, 2=retirada, 3=cancelada, 4=vencida)",
  dependencies=[admin_required]
)
async def get_reservations_paginated(
  request: Request,
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  id_status: int = Query(default=0),
  db: AsyncSession = Depends(get_db_async)
):
  filter = ReservationFilterDTO(id_status=id_status) if id_status > 0 else None

  pagination_request = PaginationRequestDTO[ReservationFilterDTO](
    page=page,
    limit=limit,
    search=search or "",
    filter=filter
  )

  pagination_response = await service.get_all_pagination(db, pagination_request)

  if pagination_response.pages > pagination_response.page:
    pagination_response.next = str(request.url.include_query_params(page=pagination_response.page + 1, limit=limit))
  if pagination_response.page > 1:
    pagination_response.prev = str(request.url.include_query_params(page=pagination_response.page - 1, limit=limit))

  return pagination_response


# -----------------------------------------------------------------
# GET USER RESERVATIONS PAGINATION (Usuario actual)
@router.get(
  "/pagination/user",
  response_model=PaginationResponseDTO[List[ReservationDetailDTO]],
  status_code=HTTP_200_OK,
  summary="Listar mis reservas con paginación",
  description="Retorna lista paginada de reservas por usuario. Filtros: id_status (1=pendiente, 2=retirada, 3=cancelada, 4=vencida)",
  dependencies=[user_required]
)
async def get_my_reservations_paginated(
  request: Request,
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  id_status: int = Query(default=0),
  current_user: dict = Depends(get_current_user()),
  db: AsyncSession = Depends(get_db_async)
):
  user_id = UUID(current_user["sub"])

  filter = ReservationFilterDTO(id_status=id_status) if id_status > 0 else None

  pagination_request = PaginationRequestDTO[ReservationFilterDTO](
    page=page,
    limit=limit,
    search=search or "",
    filter=filter
  )

  pagination_response = await service.get_all_pagination_by_user(db, user_id, pagination_request)

  if pagination_response.pages > pagination_response.page:
    pagination_response.next = str(request.url.include_query_params(page=pagination_response.page + 1, limit=limit))
  if pagination_response.page > 1:
    pagination_response.prev = str(request.url.include_query_params(page=pagination_response.page - 1, limit=limit))

  return pagination_response


# -----------------------------------------------------------------
# GET BY ID
@router.get(
  "/{id}",
  response_model=ReservationDetailDTO,
  status_code=HTTP_200_OK,
  summary="Obtener una reserva por ID",
  description="Retorna los detalles completos de una reserva específica por su ID",
  dependencies=[user_or_admin_required]
)
async def get_reservation_by_id(
  id: int,
  db: AsyncSession = Depends(get_db_async)
):
  res = await service.get_by_id(db, id)
  if not res:
    raise NotFoundError(entity="Reserva")
  return res


# -----------------------------------------------------------------
# CREATE
@router.post(
  "/",
  response_model=ReservationDTO,
  status_code=HTTP_201_CREATED,
  summary="Crear una nueva reserva",
  description="Crea una nueva reserva. La fecha de expiración se calcula automáticamente según las políticas de préstamo",
  dependencies=[user_or_admin_required]
)
async def create_reservation(
  dto: CreateReservationDTO,
  db: AsyncSession = Depends(get_db_async),
  current_user: dict = Depends(get_current_user()),
):
  res = await service.create(db, current_user["sub"], dto)
  return res


# -----------------------------------------------------------------
# UPDATE - MARK AS PICKUP
@router.put(
  "/{id}/pickup",
  response_model=ReservationDTO,
  status_code=HTTP_200_OK,
  summary="Marcar reserva como retirada (libro recogido)",
  description="Confirma el retiro de una reserva y crea automáticamente un préstamo. Requiere verificación del ejemplar físico",
  dependencies=[admin_required]
)
async def mark_reservation_as_pickup(
  id: int,
  dto: ReservationPickupDTO,
  db: AsyncSession = Depends(get_db_async)
):
  res = await service.mark_as_pickup(db, id, dto.copy_id)
  if not res:
    raise NotFoundError(entity="Reserva")
  return res


# -----------------------------------------------------------------
# UPDATE - CANCEL
@router.put(
  "/{id}/cancel",
  response_model=ReservationDTO,
  status_code=HTTP_200_OK,
  summary="Cancelar una reserva (usuario dueño o admin)",
  description="Cancela una reserva pendiente. Solo el dueño de la reserva o un administrador pueden cancelarla",
  dependencies=[user_or_admin_required]
)
async def cancel_reservation(
  id: int,
  db: AsyncSession = Depends(get_db_async),
  current_user: dict = Depends(get_current_user()),
):
  reservation = await service.get_by_id(db, id)
  if not reservation:
    raise NotFoundError(entity="Reserva")

  is_admin = current_user.get("role") == UserRole.ADMIN.value
  is_owner = str(reservation.user_id) == current_user["sub"]

  if not is_admin and not is_owner:
    raise ForbiddenError(message="No puedes cancelar esta reserva")

  res = await service.mark_as_cancelled(db, id)
  return res


# -----------------------------------------------------------------
# UPDATE - EXPIRE OVERDUE
@router.put(
  "/expire-overdue",
  response_model=int,
  status_code=HTTP_200_OK,
  summary="Marcar como vencidas las reservas cuya fecha límite pasó",
  description="Actualiza el estado de reservas vencidas (fecha límite pasada y no retiradas) a estado vencida",
  dependencies=[admin_required]
)
async def expire_overdue_reservations(db: AsyncSession = Depends(get_db_async)):
  count = await service.expire_overdue_reservations(db)
  return count