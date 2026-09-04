
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.core.security import get_current_user
from src.core.roles import UserRole
from src.core.database import get_db_async
from src.schemas.dtos import AdminStatsResponse, UserStatsResponse
from . import service

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
  response_model=AdminStatsResponse,
  status_code=HTTP_200_OK,
  summary="Estadísticas del panel de administración",
  description="Retorna conteos de reservas, préstamos, libros, usuarios y noticias",
  dependencies=[admin_required],
)
async def get_admin_stats_endpoint(db: AsyncSession = Depends(get_db_async)):
  res = await service.get_admin_stats(db)
  return res


# -----------------------------------------------------------------
# GET USER STATS
@router.get(
  "/user-stats",
  response_model=UserStatsResponse,
  status_code=HTTP_200_OK,
  summary="Estadísticas del usuario autenticado",
  description="Retorna estadísticas de préstamos del usuario actual",
  dependencies=[user_or_admin_required],
)
async def get_user_stats_endpoint(
  current_user: dict = Depends(get_current_user()),
  db: AsyncSession = Depends(get_db_async),
):
  user_id = UUID(current_user["sub"])
  res = await service.get_user_stats(db, user_id)
  return res
