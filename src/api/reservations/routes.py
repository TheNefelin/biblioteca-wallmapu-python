from typing import List
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
  prefix="/reservations",
  tags=["reservations"],
)


# -----------------------------------------------------------------
# GET ALL PAGINATION
@router.get(
  "/pagination",
  response_model=ApiResponse[PaginationResponseDTO[List[dtos.ReservationDetailDTO]]],
  status_code=HTTP_200_OK,
  summary="Listar todas las reservas con paginación",
  description="Retorna lista paginada de reservas. Filtros: id_status (1=pendiente, 2=retirada, 3=cancelada, 4=vencida)",
  #dependencies=[admin_required]
)
def get_reservations_paginated(
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  id_status: int = Query(default=0),
  db: Session = Depends(get_db)
):
  try:
    filter = dtos.ReservationFilterDTO(id_status=id_status) if id_status > 0 else None
    
    pagination_request = PaginationRequestDTO[dtos.ReservationFilterDTO](
      page=page,
      limit=limit,
      search=search or "",
      filter=filter
    )

    pagination_response = service.get_all_pagination(db, pagination_request)
    return ApiResponse.success(data=pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET USER RESERVATIONS PAGINATION (Usuario actual)
@router.get(
  "/pagination/user",
  response_model=ApiResponse[PaginationResponseDTO[List[dtos.ReservationDetailDTO]]],
  status_code=HTTP_200_OK,
  summary="Listar mis reservas con paginación",
  description="Retorna lista paginada de reservas por usuario. Filtros: id_status (1=pendiente, 2=retirada, 3=cancelada, 4=vencida)",
  dependencies=[user_required]
)
def get_my_reservations_paginated(
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  id_status: int = Query(default=0),
  current_user = Depends(get_current_user()),
  db: Session = Depends(get_db)
):
  try:
    user_id = UUID(current_user["sub"])
    
    filter = dtos.ReservationFilterDTO(id_status=id_status) if id_status > 0 else None
    
    pagination_request = PaginationRequestDTO[dtos.ReservationFilterDTO](
      page=page,
      limit=limit,
      search=search or "",
      filter=filter
    )
    
    pagination_response = service.get_user_pagination(db, user_id, pagination_request)
    return ApiResponse.success(data=pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET BY ID
@router.get(
  "/{id}",
  response_model=ApiResponse[dtos.ReservationDetailDTO],
  status_code=HTTP_200_OK,
  summary="Obtener una reserva por ID",
  description="Retorna los detalles completos de una reserva específica por su ID",
  dependencies=[admin_required]
)
def get_reservation_by_id(
  id: int,
  db: Session = Depends(get_db)
):
  res = service.get_by_id(db, id)
  if not res:
    return ApiResponse.not_found(message="Reserva no encontrada")
  return ApiResponse.success(data=res)


# -----------------------------------------------------------------
# CREATE
@router.post(
  "/",
  response_model=ApiResponse[dtos.ReservationDetailDTO],
  status_code=HTTP_201_CREATED,
  summary="Crear una nueva reserva",
  description="Crea una nueva reserva. La fecha de expiración se calcula automáticamente según las políticas de préstamo",
  dependencies=[user_or_admin_required]
)
def create_reservation(
  dto: dtos.CreateReservationDTO,
  db: Session = Depends(get_db),
  current_user = Depends(get_current_user())
):
  res = service.create(db, current_user["sub"], dto)
  return ApiResponse.created(data=res, message="Reserva creada exitosamente")


# -----------------------------------------------------------------
# UPDATE - MARK AS PICKUP
@router.put(
  "/{id}/pickup",
  response_model=ApiResponse[dtos.ReservationDetailDTO],
  status_code=HTTP_200_OK,
  summary="Marcar reserva como retirada (libro recogido)",
  description="Confirma el retiro de una reserva y crea automáticamente un préstamo. Requiere verificación del ejemplar físico",
  dependencies=[admin_required]
)
def mark_reservation_as_pickup(
  id: int,
  dto: dtos.ReservationPickupDTO,
  db: Session = Depends(get_db)
):
  try:
    res = service.mark_as_pickup(db, id, dto.copy_id)
    if not res:
      return ApiResponse.not_found(message="Reserva no encontrada")
    return ApiResponse.success(data=res, message="Reserva marcada como retirada")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# UPDATE - CANCEL
@router.put(
  "/{id}/cancel",
  response_model=ApiResponse[dtos.ReservationDetailDTO],
  status_code=HTTP_200_OK,
  summary="Cancelar una reserva (usuario dueño o admin)",
  description="Cancela una reserva pendiente. Solo el dueño de la reserva o un administrador pueden cancelarla",
  dependencies=[user_or_admin_required]
)
def cancel_reservation(
  id: int,
  db: Session = Depends(get_db),
  current_user = Depends(get_current_user())
):
  try:
    reservation = service.get_by_id(db, id)
    if not reservation:
      return ApiResponse.not_found(message="Reserva no encontrada")

    is_admin = current_user.get("role") == UserRole.ADMIN.value
    is_owner = str(reservation.user_id) == current_user["sub"]

    if not is_admin and not is_owner:
      return ApiResponse.forbidden(message="No puedes cancelar esta reserva")

    res = service.mark_as_cancelled(db, id)
    return ApiResponse.success(data=res, message="Reserva cancelada")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# UPDATE - EXPIRE OVERDUE
@router.put(
  "/expire-overdue",
  response_model=ApiResponse[int],
  status_code=HTTP_200_OK,
  summary="Marcar como vencidas las reservas cuya fecha límite pasó",
  description="Actualiza el estado de reservas vencidas (fecha límite pasada y no retiradas) a estado vencida",
  dependencies=[admin_required]
)
def expire_overdue_reservations(db: Session = Depends(get_db)):
  count = service.expire_overdue_reservations(db)
  return ApiResponse.success(data=count, message=f"{count} reservas marcadas como vencidas")



