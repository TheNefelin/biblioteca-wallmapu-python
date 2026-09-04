from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import AdminStatsResponse, UserStatsResponse
from . import repository

# -----------------------------------------------------------------
# GET ADMIN STATS
async def get_admin_stats(db: AsyncSession) -> AdminStatsResponse:
  data = await repository.get_admin_stats(db)
  return AdminStatsResponse(**data)


# -----------------------------------------------------------------
# GET USER STATS
async def get_user_stats(db: AsyncSession, user_id: UUID) -> UserStatsResponse:
  data = await repository.get_user_stats(db, user_id)
  return UserStatsResponse(**data)
