import os
from sqlalchemy.orm import Session
from typing import List
import uuid

from src.api.news_gallery.dtos import CreateNewsGalleryDTO
from src.api.news_gallery.models import NewsGallery
from src.api.news_gallery.repository import create
from src.services.image_service import save_image_webp


STATIC_PATH = "static/news"

def create_news_gallery_with_images(
    news_id: int,
    files: List,
    alts: List,
    db: Session
):
  saved_files = []
  created_items = []

  try:
    for file, alt in zip(files, alts):
      filename = f"{news_id}_{uuid.uuid4().hex}.webp"
      save_image_webp(file.file.read(), filename)

      gallery = NewsGallery(
        news_id=news_id,
        alt=alt,
        img=filename
      )
      db.add(gallery)

      saved_files.append(filename)
      created_items.append(gallery)

    db.commit()

    for item in created_items:
      db.refresh(item)

    return created_items    
  except Exception as e:
    db.rollback()

    # 🔥 rollback físico
    for filename in saved_files:
      path = os.path.join(STATIC_PATH, filename)
      if os.path.exists(path):
        os.remove(path)
        
    raise e
