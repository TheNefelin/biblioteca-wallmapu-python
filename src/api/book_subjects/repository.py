from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


# -----------------------------------------------------------------
# UPDATE (reemplaza relaciones; si subject_ids viene vacío, solo elimina)
async def update(db: AsyncSession, id_book: int, subject_ids: list[int]) -> list[models.BookSubject]:
  await db.execute(
    delete(models.BookSubject).where(models.BookSubject.id_book == id_book)
  )

  relations = [
    models.BookSubject(id_book=id_book, id_subject=sid)
    for sid in subject_ids
  ]

  if relations:
    db.add_all(relations)

  await db.commit()

  return relations


# -----------------------------------------------------------------
# DELETE
async def delete(db: AsyncSession, id_book: int, id_subject: int) -> bool:
  relation = await db.get(
    models.BookSubject,
    (id_book, id_subject)
  )

  if not relation:
    return False

  await db.delete(relation)
  await db.commit()

  return True


# -----------------------------------------------------------------
# GET BY BOOK
async def get_by_book(db: AsyncSession, id_book: int) -> list[models.BookSubject]:
  result = await db.execute(
    select(models.BookSubject).where(models.BookSubject.id_book == id_book)
  )
  return list(result.scalars().all())


# -----------------------------------------------------------------
# DELETE BY ID BOOK
async def delete_by_book(db: AsyncSession, id_book: int) -> bool:
  result = await db.execute(
    delete(models.BookSubject).where(models.BookSubject.id_book == id_book)
  )

  await db.commit()

  return result.rowcount > 0