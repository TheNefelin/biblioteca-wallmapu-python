from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import CopyStatus


# -----------------------------------------------------------------
# GET ALL
async def get_all(db: AsyncSession) -> list[CopyStatus]:
  result = await db.execute(select(CopyStatus).order_by(CopyStatus.name.asc()))
  return list(result.scalars().all())


# -----------------------------------------------------------------
# GET BY ID
async def get_by_id(db: AsyncSession, status_id: int) -> CopyStatus | None:
  result = await db.execute(select(CopyStatus).where(CopyStatus.id_status == status_id))
  return result.scalar_one_or_none()
