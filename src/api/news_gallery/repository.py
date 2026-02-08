from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.news.models import News
from src.api.news_gallery.dtos import CreateNewsGalleryDTO
from src.api.news_gallery.models import NewsGallery

def get_all(db: Session):
  try:
    return db.query(NewsGallery).all()
  except SQLAlchemyError as e:
    raise e

def get_by_id(id: int, db: Session):
  try:
    return db.query(NewsGallery).filter(NewsGallery.id_news_gallery == id).first()
  except SQLAlchemyError as e:
    raise e

def get_by_news_id(id_news: int, db: Session):
  try:
    return db.query(NewsGallery).filter(NewsGallery.news_id == id_news).all()
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

