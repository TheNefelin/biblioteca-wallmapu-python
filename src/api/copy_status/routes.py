from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.core.database import get_db_async
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.schemas.dtos import CopyStatusDTO
from src.shared.dtos import ApiResponse
from . import service


admin_or_user_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(
  prefix="/copy-status",
  tags=["copy-status"],
  dependencies=[admin_or_user_required]
)


# -----------------------------------------------------------------
@router.get(
  "/",
  response_model=ApiResponse[List[CopyStatusDTO]],
  status_code=HTTP_200_OK,
  summary="Listar estados de ejemplar",
  description="Retorna todos los estados de ejemplar para selects",
)
async def get_all_copy_status(db: AsyncSession = Depends(get_db_async)):
  try:
    res = await service.get_all(db)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))
