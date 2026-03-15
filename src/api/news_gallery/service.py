from sqlalchemy.orm import Session
from typing import List

from src.api.news_gallery.models import NewsGallery
from src.services import cloudinary_service

#STATIC_PATH = "static/news"
PATH = "news"

def create_news_gallery_with_images(
    news_id: int,
    files: List,
    alts: List,
    db: Session
):
  #saved_files = []
  uploaded_public_ids = []
  created_items = []

  try:
    for file, alt in zip(files, alts):
      #filename = f"{news_id}_{uuid.uuid4().hex}.webp"
      #save_image_webp(file.file.read(), filename)

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

      #saved_files.append(url)
      uploaded_public_ids.append(public_id)
      created_items.append(gallery)

    db.commit()

    for item in created_items:
      db.refresh(item)

    return created_items    
  except Exception as e:
    db.rollback()

    # 🔥 rollback físico en Cloudinary
    for public_id in uploaded_public_ids:
      try:
        cloudinary_service.delete_image(public_id)
      except Exception:
        pass  # opcional: loggear error    

    raise e
    
    # 🔥 rollback físico
    #for filename in saved_files:
    #  path = os.path.join(STATIC_PATH, filename)
    #  if os.path.exists(path):
    #    os.remove(path)
        
def delete_news_gallery_by_news_id(
  news_id: int,
  db: Session
) -> int:
  try:
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
  except Exception as e:
    db.rollback()
    raise e

def delete_news_gallery(
    id: int,
    db: Session
) -> int:
  try:
    item = db.query(NewsGallery).filter(NewsGallery.id_news_gallery == id).first()

    if not item:
      return 0

    # 1️⃣ borrar imagen en Cloudinary
    # extraemos public_id desde la URL
    public_id = cloudinary_service.extract_public_id(item.url)

    if public_id:
      cloudinary_service.delete_image(public_id)

    # 2️⃣ borrar registro DB
    db.delete(item)
    db.commit()
    return 1
  except Exception as e:
    db.rollback()
    raise e
