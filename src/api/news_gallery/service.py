from sqlalchemy.orm import Session
from typing import List

from src.api.news import repository as news_repository
from src.api.news_gallery.models import NewsGallery
from src.services import cloudinary_service
from . import dtos, repository

PATH = "news"


def get_by_news_id(db: Session, news_id: int) -> list[dtos.NewsGalleryDTO]:
  items = repository.get_by_news_id(db, news_id)
  return [dtos.NewsGalleryDTO.model_validate(item) for item in items]


def create(db: Session, news_id: int, url: str, alt: str = "") -> dtos.NewsGalleryDTO:
  news = news_repository.get_by_id(db, news_id)
  if not news:
    raise ValueError(f"La noticia con id {news_id} no existe")
  
  item = repository.create(db, {"news_id": news_id, "url": url, "alt": alt})
  return dtos.NewsGalleryDTO.model_validate(item)


def create_news_gallery_with_images(
    db: Session,
    news_id: int,
    files: List,
    alts: List,
):
  news = news_repository.get_by_id(db, news_id)
  if not news:
    raise ValueError(f"La noticia con id {news_id} no existe")
  
  uploaded_public_ids = []
  created_items = []

  try:
    for file, alt in zip(files, alts):
      url, public_id = cloudinary_service.upload_image_16_9(
        file_bytes=file.file.read(),
        folder=f"{PATH}"
      )

      gallery = NewsGallery(
        news_id=news_id,
        alt=alt,
        url=url
      )
      db.add(gallery)

      uploaded_public_ids.append(public_id)
      created_items.append(gallery)

    db.commit()

    for item in created_items:
      db.refresh(item)

    return created_items    
  except Exception as e:
    db.rollback()

    for public_id in uploaded_public_ids:
      try:
        cloudinary_service.delete_image(public_id)
      except Exception:
        pass    

    raise e


def delete_news_gallery_by_news_id(db: Session, news_id: int) -> int:
  items = db.query(NewsGallery).filter(
    NewsGallery.news_id == news_id
  ).all()

  for item in items:
    public_id = cloudinary_service.extract_public_id(item.url)

    if public_id:
      cloudinary_service.delete_image(public_id)

    db.delete(item)

  db.commit()
  return len(items)


def delete_news_gallery(db: Session, id: int) -> int:
  item = db.query(NewsGallery).filter(NewsGallery.id_news_gallery == id).first()

  if not item:
    return 0

  public_id = cloudinary_service.extract_public_id(item.url)

  if public_id:
    cloudinary_service.delete_image(public_id)

  db.delete(item)
  db.commit()
  return 1