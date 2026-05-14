from sqlalchemy.orm import Session

from . import models


# -----------------------------------------------------------------
# GET ALL
def get_by_news_id(db: Session, news_id: int) -> list[models.NewsGallery]:
  return (db
    .query(models.NewsGallery)
    .filter(models.NewsGallery.news_id == news_id)
    .order_by(models.NewsGallery.id_news_gallery.desc())
    .all()
  )


# -----------------------------------------------------------------
# CREATE
def create(db: Session, data: dict) -> models.NewsGallery:
  new_item = models.NewsGallery(**data)
  db.add(new_item)
  db.commit()
  db.refresh(new_item)
  return new_item


# -----------------------------------------------------------------
# DELETE BY ID NEWS
def delete_by_news_id(db: Session, news_id: int) -> bool:
  items = (
    db.query(models.NewsGallery)
    .filter(models.NewsGallery.news_id == news_id)
    .all()
  )

  for item in items:
    db.delete(item)
  
  db.commit()
  return True


# -----------------------------------------------------------------
# DELETE BY ID GALLERY
def delete(db: Session, id: int) -> bool:
  item = (
    db.query(models.NewsGallery)
    .filter(models.NewsGallery.id_news_gallery == id)
    .first()
  )
  
  if not item:
    return False

  db.delete(item)
  db.commit()
  return True