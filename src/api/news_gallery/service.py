from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.api.news import repository as news_repository
from src.models import models
from src.schemas.dtos import NewsGalleryDTO
from src.core import cloudinary
from . import repository

PATH = "news"


async def get_by_news_id(db: AsyncSession, news_id: int) -> list[NewsGalleryDTO]:
  items = await repository.get_by_news_id(db, news_id)
  return [NewsGalleryDTO.model_validate(item) for item in items]


async def create(db: AsyncSession, news_id: int, url: str, alt: str = "") -> NewsGalleryDTO:
  news = await news_repository.get_by_id(db, news_id)
  if not news:
    raise ValueError(f"La noticia con id {news_id} no existe")

  item = await repository.create(db, {"news_id": news_id, "url": url, "alt": alt})
  return NewsGalleryDTO.model_validate(item)


async def create_news_gallery_with_images(
    db: AsyncSession,
    news_id: int,
    files: List,
    alts: List,
):
  news = await news_repository.get_by_id(db, news_id)
  if not news:
    raise ValueError(f"La noticia con id {news_id} no existe")

  uploaded_public_ids = []
  created_items = []

  try:
    for file, alt in zip(files, alts):
      file_bytes = await file.read()
      url, public_id = cloudinary.upload_image_16_9(
        file_bytes=file_bytes,
        folder=f"{PATH}"
      )

      gallery = models.NewsGallery(
        news_id=news_id,
        alt=alt,
        url=url
      )
      db.add(gallery)

      uploaded_public_ids.append(public_id)
      created_items.append(gallery)

    await db.commit()

    for item in created_items:
      await db.refresh(item)

    return created_items
  except Exception as e:
    await db.rollback()

    for public_id in uploaded_public_ids:
      try:
        cloudinary.delete_image(public_id)
      except Exception:
        pass

    raise e


async def delete_news_gallery_by_news_id(db: AsyncSession, news_id: int) -> int:
  items = await repository.get_by_news_id(db, news_id)

  for item in items:
    public_id = cloudinary.extract_public_id(item.url)
    if public_id:
      cloudinary.delete_image(public_id)

  await repository.delete_by_news_id(db, news_id)
  return len(items)


async def delete_news_gallery(db: AsyncSession, id: int) -> bool:
  item = await repository.get_by_id(db, id)

  if not item:
    return False

  public_id = cloudinary.extract_public_id(item.url)
  if public_id:
    cloudinary.delete_image(public_id)

  await repository.delete(db, id)
  return True