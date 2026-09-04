from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import UserRole


# -----------------------------------------------------------------
# GET ALL
async def get_all(db: AsyncSession) -> list[UserRole]:
  result = await db.execute(select(UserRole).order_by(UserRole.id_user_role.asc()))
  return list(result.scalars().all())
