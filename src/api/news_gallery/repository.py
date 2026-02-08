from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.news.models import News
from src.api.news_gallery.dtos import CreateNewsGalleryDTO
from src.api.news_gallery.models import NewsGallery


def get_by_news_id(news_id: int, db: Session):
  try:
    return db.query(NewsGallery).filter(NewsGallery.news_id == news_id).all()
  except SQLAlchemyError as e:
    raise e

def create(data: CreateNewsGalleryDTO, db: Session):
  try:
    # Verificar que la noticia exista
    news_exists = db.query(News).filter(News.id_news == data.news_id).first()
    if not news_exists:
      raise ValueError(f"La noticia con id {data.news_id} no existe")

    new_item = NewsGallery(**data.model_dump())
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

def delete_by_news_id(news_id: int, db: Session):
  try:
    items = db.query(NewsGallery).filter(NewsGallery.news_id == news_id).all()

    for item in items:
      db.delete(item)
      
    db.commit()
    return len(items)
  except SQLAlchemyError as e:
    db.rollback()
    raise e

def delete(id: int, db: Session):
  try:
    item = db.query(NewsGallery).filter(NewsGallery.id_news_gallery == id).first()
    
    if not item:
      return 0

    db.delete(item)
    db.commit()
    return 1
  except SQLAlchemyError as e:
    db.rollback()
    raise e