from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.news_gallery import dtos, models

def get_all(db: Session):
  try:
    return db.query(models.NewsGallery).all()
  except SQLAlchemyError as e:
    raise e

def get_by_id(id: int, db: Session):
  try:
    return db.query(models.NewsGallery).filter(models.NewsGallery.id_news_gallery == id).first()
  except SQLAlchemyError as e:
    raise e

def get_by_news_id(db: Session, id_news: int):
  try:
    return db.query(models.NewsGallery).filter(models.NewsGallery.news_id == id_news).all()
  except SQLAlchemyError as e:
    raise e

def create(db: Session, data: dtos.CreateGalleryDTO):
  try:
    new_item = models.News(**data.model_dump())
    
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

def delete(db: Session, id: int):
  return db.query(models.NewsGallery).filter(models.NewsGallery.id_news_gallery == id).delete()