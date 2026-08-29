from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


# -----------------------------------------------------------------
# GET DEFAULT
async def get_default_policy(db: AsyncSession) -> models.LoanPolicy | None:
  result = await db.execute(select(models.LoanPolicy))
  return result.scalars().first()


# -----------------------------------------------------------------
# UPDATE
async def update_policy(db: AsyncSession, id: int, data: dict) -> models.LoanPolicy | None:
  result = await db.execute(
    select(models.LoanPolicy).where(models.LoanPolicy.id_policy == id)
  )
  policy = result.scalar_one_or_none()

  if not policy:
    return None

  for key, value in data.items():
    setattr(policy, key, value)

  await db.commit()
  await db.refresh(policy)

  return policy