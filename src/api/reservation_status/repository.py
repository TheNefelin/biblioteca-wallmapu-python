from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import ReservationStatus


# -----------------------------------------------------------------
# GET ALL
async def get_all(db: AsyncSession) -> list[ReservationStatus]:
  result = await db.execute(select(ReservationStatus).order_by(ReservationStatus.id_status.asc()))
  return list(result.scalars().all())
