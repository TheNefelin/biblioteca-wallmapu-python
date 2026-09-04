from sqlalchemy import delete as sqla_delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


# -----------------------------------------------------------------
# UPDATE
async def update(db: AsyncSession, id_book: int, author_ids: list[int]) -> list[models.BookAuthor]:
  await db.execute(
    sqla_delete(models.BookAuthor).where(models.BookAuthor.id_book == id_book)
  )

  relations = [
    models.BookAuthor(id_book=id_book, id_author=aid)
    for aid in author_ids
  ]

  if relations:
    db.add_all(relations)

  await db.commit()

  return await get_by_book(db, id_book)


# -----------------------------------------------------------------
# DELETE
async def delete(db: AsyncSession, id_book: int, id_author: int) -> bool:
  relation = await db.get(
    models.BookAuthor,
    (id_book, id_author)
  )

  if not relation:
    return False

  await db.delete(relation)
  await db.commit()

  return True


# -----------------------------------------------------------------
# GET BY BOOK
async def get_by_book(db: AsyncSession, id_book: int) -> list[models.BookAuthor]:
  result = await db.execute(
    select(models.BookAuthor).where(models.BookAuthor.id_book == id_book)
  )
  return list(result.scalars().all())


# -----------------------------------------------------------------
# DELETE BY ID BOOK
async def delete_by_book(db: AsyncSession, id_book: int) -> bool:
  result = await db.execute(
    sqla_delete(models.BookAuthor).where(models.BookAuthor.id_book == id_book)
  )

  await db.commit()

  return result.rowcount > 0