import os
from sqlalchemy.orm import Session
from typing import List

from src.api.news_gallery.models import NewsGallery
#from src.services.image_service import save_image_webp
from src.services.cloudinary_service import upload_image_16_9

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
      #filename = f"{news_id}_{uuid.uuid4().hex}.webp"
      #save_image_webp(file.file.read(), filename)

      url = upload_image_16_9(
        file_bytes=file.file.read(),
        folder=f"news/{news_id}"
      )

      gallery = NewsGallery(
        news_id=news_id,
        alt=alt,
        url=url
      )
      db.add(gallery)

      saved_files.append(url)
      created_items.append(gallery)

    db.commit()

    for item in created_items:
      db.refresh(item)

    return created_items    
  except Exception as e:
    db.rollback()

    # 🔥 rollback físico
    #for filename in saved_files:
    #  path = os.path.join(STATIC_PATH, filename)
    #  if os.path.exists(path):
    #    os.remove(path)
        
    raise e
