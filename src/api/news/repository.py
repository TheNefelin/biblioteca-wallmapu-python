from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.news import dtos, models

def get_all(db: Session):
  try:
    return db.query(models.News).all()
  except SQLAlchemyError as e:
    raise e

def create(db: Session, data: dtos.CreateNewsDTO):
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

def update(db: Session, id: int, data: dtos.UpdateNewsDTO):
  try:
    item = db.query(models.News).filter(models.News.id_news == id).first()
    if not item:
      return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
      setattr(item, key, value)
    
    db.commit()
    db.refresh(item)
    return item
  except IntegrityError as e:
    db.rollback()
    raise ValueError("Error de integridad en la base de datos")  
  except SQLAlchemyError as e:
    db.rollback()
    raise e
  