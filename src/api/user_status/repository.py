from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import UserStatus


# -----------------------------------------------------------------
# GET ALL
async def get_all(db: AsyncSession) -> list[UserStatus]:
  result = await db.execute(select(UserStatus).order_by(UserStatus.id_user_status.asc()))
  return list(result.scalars().all())
