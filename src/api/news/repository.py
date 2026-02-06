from math import ceil
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from src.api.news import dtos, models

def get_all_pagination(page: int, page_size: int, search: str | None, db: Session):
  try:
    # Query base con eager loading de imágenes
    query = db.query(models.News).options(joinedload(models.News.images))
    
    # Aplicar filtro de búsqueda si existe
    if search:
      search_filter = or_(
        models.News.title.ilike(f"%{search}%"),
        models.News.subtitle.ilike(f"%{search}%")
      )
      query = query.filter(search_filter)
    
    # Total de registros
    count = query.count()
    
    # Total de páginas
    pages = ceil(count / page_size) if count > 0 else 0
    
    # Calcular offset
    skip = (page - 1) * page_size
    
    # Obtener registros paginados
    result = (
      query
      .order_by(models.News.created_at.desc())
      .offset(skip)
      .limit(page_size)
      .all()
    )
    
    return count, pages, result
  except SQLAlchemyError as e:
    raise e

def get_by_id(id: int, db: Session):
  try:
    return db.query(models.News).filter(models.News.id_news == id).first()
  except SQLAlchemyError as e:
    raise e

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
  