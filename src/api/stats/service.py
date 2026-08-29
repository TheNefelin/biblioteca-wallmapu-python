from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import AdminStatsDTO, UserStatsDTO
from . import repository

# -----------------------------------------------------------------
# GET ADMIN STATS
async def get_admin_stats(db: AsyncSession) -> AdminStatsDTO:
  data = await repository.get_admin_stats(db)
  return AdminStatsDTO(**data)


# -----------------------------------------------------------------
# GET USER STATS
async def get_user_stats(db: AsyncSession, user_id: UUID) -> UserStatsDTO:
  data = await repository.get_user_stats(db, user_id)
  return UserStatsDTO(**data)
