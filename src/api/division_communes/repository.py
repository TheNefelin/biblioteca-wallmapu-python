from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import Commune


# -----------------------------------------------------------------
# GET ALL
async def get_all(db: AsyncSession) -> list[Commune]:
  result = await db.execute(select(Commune).order_by(Commune.name.asc()))
  return list(result.scalars().all())
