
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.core.database import get_db
from src.shared.dtos import ApiResponse
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))
user_or_admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(
  prefix="/stat",
  tags=["stat"], 
)


# -----------------------------------------------------------------
# GET ADMIN STATS
@router.get(
  "/admin-stats", 
  response_model=ApiResponse[dtos.AdminStatsDTO],
  status_code=HTTP_200_OK,
  summary="Estadísticas del panel de administración",
  description="Retorna conteos de reservas, préstamos, libros, usuarios y noticias",
  dependencies=[admin_required],
)
def get_admin_stats_endpoint(db: Session = Depends(get_db)):
  try:
    res = service.get_admin_stats(db)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET USER STATS
@router.get(
  "/user-stats",
  response_model=ApiResponse[dtos.UserStatsDTO],
  status_code=HTTP_200_OK,
  summary="Estadísticas del usuario autenticado",
  description="Retorna estadísticas de préstamos del usuario actual",
  dependencies=[user_or_admin_required],
)
def get_user_stats_endpoint(
  current_user: dict = Depends(get_current_user()),
  db: Session = Depends(get_db),
):
  try:
    user_id = UUID(current_user["sub"])
    res = service.get_user_stats(db, user_id)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))