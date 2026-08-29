from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import models


# -----------------------------------------------------------------
# GET ALL
async def get_by_news_id(db: AsyncSession, news_id: int) -> list[models.NewsGallery]:
  result = await db.execute(
    select(models.NewsGallery)
    .where(models.NewsGallery.news_id == news_id)
    .order_by(models.NewsGallery.id_news_gallery.desc())
  )
  return list(result.scalars().all())


# -----------------------------------------------------------------
# GET BY ID
async def get_by_id(db: AsyncSession, id: int):
  result = await db.execute(
    select(models.NewsGallery).where(models.NewsGallery.id_news_gallery == id)
  )
  return result.scalar_one_or_none()


# -----------------------------------------------------------------
# CREATE
async def create(db: AsyncSession, data: dict) -> models.NewsGallery:
  new_item = models.NewsGallery(**data)
  db.add(new_item)
  await db.commit()
  await db.refresh(new_item)
  return new_item


# -----------------------------------------------------------------
# DELETE BY ID NEWS
async def delete_by_news_id(db: AsyncSession, news_id: int) -> bool:
  items = (await db.execute(
    select(models.NewsGallery).where(models.NewsGallery.news_id == news_id)
  )).scalars().all()

  for item in items:
    await db.delete(item)

  await db.commit()
  return True


# -----------------------------------------------------------------
# DELETE BY ID GALLERY
async def delete(db: AsyncSession, id: int) -> bool:
  item = (await db.execute(
    select(models.NewsGallery).where(models.NewsGallery.id_news_gallery == id)
  )).scalar_one_or_none()

  if not item:
    return False

  await db.delete(item)
  await db.commit()
  return True