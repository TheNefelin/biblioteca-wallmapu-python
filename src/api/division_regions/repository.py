from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Region


# -----------------------------------------------------------------
# GET ALL
async def get_all(db: AsyncSession) -> list[Region]:
  result = await db.execute(select(Region).order_by(Region.region.asc()))
  return list(result.scalars().all())
