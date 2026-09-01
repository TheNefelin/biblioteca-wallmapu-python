from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.core.database import get_db_async
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.schemas.dtos import UserStatusDTO
from . import service

admin_or_user_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(prefix="/user-status", tags=["user-status"], dependencies=[admin_or_user_required])

# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/",
  response_model=List[UserStatusDTO],
  status_code=HTTP_200_OK,
  summary="Listar estados de usuario",
  description="Obtiene lista completa de estados de usuario ordenada por ID",
)
async def get_all_status(db: AsyncSession = Depends(get_db_async)):
  res = await service.get_all(db)
  return res
