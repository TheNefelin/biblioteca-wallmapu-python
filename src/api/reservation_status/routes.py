from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.core.database import get_db_async
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.schemas.dtos import ReservationStatusDTO
from . import service

user_or_admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(
  prefix="/reservation-status",
  tags=["reservation-status"],
  dependencies=[user_or_admin_required]
)

# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/",
  response_model=List[ReservationStatusDTO],
  status_code=HTTP_200_OK
)
async def get_all_reservation_status(db: AsyncSession = Depends(get_db_async)):
  res = await service.get_all(db)
  return res
