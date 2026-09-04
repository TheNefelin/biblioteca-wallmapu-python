from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import LoanStatus


async def get_all(db: AsyncSession) -> list[LoanStatus]:
  result = await db.execute(select(LoanStatus).order_by(LoanStatus.id_status.asc()))
  return list(result.scalars().all())
