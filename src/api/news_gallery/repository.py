from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.news.models import News
from . import models

# -----------------------------------------------------------------
# GET ALL
def get_by_news_id(news_id: int, db: Session) -> list[models.NewsGallery]:
  try:
    return (db
      .query(models.NewsGallery)
      .filter(models.NewsGallery.news_id == news_id)
      .order_by(models.NewsGallery.id_news_gallery.desc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# CREATE
def create(data: dict, db: Session) -> models.NewsGallery:
  try:
    # Verificar que la noticia exista
    news_exists = (
      db.query(News)
      .filter(News.id_news == data["news_id"])
      .first()
    )

    if not news_exists:
      raise ValueError(f"La noticia con id {data['news_id']} no existe")

    new_item = models.NewsGallery(**data)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item
  except IntegrityError as e:
    db.rollback()
    raise ValueError("Error de integridad en la base de datos")  
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------
# DELETE BY ID NEWS
def delete_by_news_id(news_id: int, db: Session) -> bool:
  try:
    items = (
      db.query(models.NewsGallery)
      .filter(models.NewsGallery.news_id == news_id)
      .all()
    )

    for item in items:
      db.delete(item)
    
    db.commit()
    return True
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------
# DELETE BY ID GALLERY
def delete(id: int, db: Session) -> bool:
  try:
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
  except SQLAlchemyError as e:
    db.rollback()
    raise e
