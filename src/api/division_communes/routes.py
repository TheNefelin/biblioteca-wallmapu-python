from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.core.database import get_db_async
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.schemas.dtos import CommuneDTO
from . import service

admin_or_user_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(prefix="/division-commune", tags=["division-commune"], dependencies=[admin_or_user_required])

# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/",
  response_model=List[CommuneDTO],
  status_code=HTTP_200_OK,
  summary="Listar comunas",
  description="Obtiene lista completa de comunas ordenada por nombre",
)
async def get_all_commune(db: AsyncSession = Depends(get_db_async)):
  res = await service.get_all(db)
  return res
