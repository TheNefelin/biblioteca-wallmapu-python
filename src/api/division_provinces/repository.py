from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Province


# -----------------------------------------------------------------
# GET ALL
async def get_all(db: AsyncSession) -> list[Province]:
  result = await db.execute(select(Province).order_by(Province.province.asc()))
  return list(result.scalars().all())
