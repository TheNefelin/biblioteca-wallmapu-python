from typing import List
from uuid import UUID
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
  prefix="/reservations",
  tags=["reservations"],
)

@router.get(
  "/",
  response_model=ApiResponse[List[dtos.ReservationDetailDTO]],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def get_all_reservations(db: Session = Depends(get_db)):
  try:
    res = service.get_all(db)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.get(
  "/user/{user_id}",
  response_model=ApiResponse[List[dtos.ReservationDetailDTO]],
  status_code=HTTP_200_OK,
  dependencies=[user_or_admin_required]
)
def get_reservations_by_user(
  user_id: UUID,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_by_user_id(db, user_id)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.get(
  "/book/{book_id}",
  response_model=ApiResponse[List[dtos.ReservationDetailDTO]],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def get_active_reservations_by_book(
  book_id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_active_by_book_id(db, book_id)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.get(
  "/{id}",
  response_model=ApiResponse[dtos.ReservationDetailDTO],
  status_code=HTTP_200_OK
)
def get_reservation_by_id(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_by_id(db, id)
    if not res:
      return ApiResponse.not_found(message="Reserva no encontrada")
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.post(
  "/",
  response_model=ApiResponse[dtos.ReservationDetailDTO],
  status_code=HTTP_201_CREATED,
  dependencies=[user_or_admin_required]
)
def create_reservation(
  dto: dtos.CreateReservationDTO,
  db: Session = Depends(get_db),
  current_user = Depends(get_current_user())
):
  try:
    res = service.create(db, current_user["sub"], dto)
    return ApiResponse.created(data=res, message="Reserva creada exitosamente")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.put(
  "/{id}/pickup",
  response_model=ApiResponse[dtos.ReservationDetailDTO],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def mark_reservation_as_pickup(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.mark_as_pickup(db, id)
    if not res:
      return ApiResponse.not_found(message="Reserva no encontrada")
    return ApiResponse.success(data=res, message="Reserva marcada como retirada")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.put(
  "/{id}/cancel",
  response_model=ApiResponse[dtos.ReservationDetailDTO],
  status_code=HTTP_200_OK,
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

    if reservation.user_id != UUID(current_user["sub"]):
      return ApiResponse.forbidden(message="No puedes cancelar esta reserva")

    res = service.mark_as_cancelled(db, id)
    return ApiResponse.success(data=res, message="Reserva cancelada")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.put(
  "/expire-overdue",
  response_model=ApiResponse[int],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def expire_overdue_reservations(db: Session = Depends(get_db)):
  try:
    count = service.expire_overdue_reservations(db)
    return ApiResponse.success(data=count, message=f"{count} reservas marcadas como vencidas")
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.delete(
  "/{id}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def delete_reservation(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.delete(db, id)
    if res is None:
      return ApiResponse.not_found(message="Reserva no encontrada")
    return ApiResponse.success(data=res, message="Reserva eliminada")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))
