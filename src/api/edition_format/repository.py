from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


# -----------------------------------------------------------------
# UPDATE
async def update(db: AsyncSession, id_edition: int, format_ids: list[int]) -> list[models.EditionFormat]:
  await db.execute(
    delete(models.EditionFormat).where(models.EditionFormat.id_edition == id_edition)
  )

  relations = [
    models.EditionFormat(id_edition=id_edition, id_format=fid)
    for fid in format_ids
  ]

  if relations:
    db.add_all(relations)

  await db.commit()

  return relations


# -----------------------------------------------------------------
# DELETE
async def delete(db: AsyncSession, id_edition: int, id_format: int) -> bool:
  relation = await db.get(
    models.EditionFormat,
    (id_edition, id_format)
  )

  if not relation:
    return False

  await db.delete(relation)
  await db.commit()

  return True


# -----------------------------------------------------------------
# GET BY EDITION
async def get_by_edition(db: AsyncSession, id_edition: int) -> list[models.EditionFormat]:
  result = await db.execute(
    select(models.EditionFormat).where(models.EditionFormat.id_edition == id_edition)
  )
  return list(result.scalars().all())


# -----------------------------------------------------------------
# DELETE BY ID EDITION
async def delete_by_edition(db: AsyncSession, id_edition: int) -> bool:
  result = await db.execute(
    delete(models.EditionFormat).where(models.EditionFormat.id_edition == id_edition)
  )

  await db.commit()

  return result.rowcount > 0