from math import ceil
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from src.api.news.dtos import CreateNewsDTO, UpdateNewsDTO
from src.api.news.models import News

# -----------------------------------------------------------------
# GET ALL Pagination
def get_all_pagination(page: int, items: int, search: str | None, db: Session):
  try:
    # Query base con eager loading de imágenes
    query = (
      db.query(News)
      .options(joinedload(News.images))
    )
    
    # Aplicar filtro de búsqueda si existe
    if search:
      search_filter = or_(
        News.title.ilike(f"%{search}%"),
        News.subtitle.ilike(f"%{search}%")
      )
      query = query.filter(search_filter)
    
    # Total de registros
    count = query.count()
    
    # Total de páginas
    pages = ceil(count / items) if count > 0 else 0
    
    # Calcular offset
    skip = (page - 1) * items
    
    # Obtener registros paginados
    result = (
      query
      .order_by(News.created_at.desc())
      .offset(skip)
      .limit(items)
      .all()
    )
    
    return count, pages, result
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# GET BY ID Pagination    
def get_by_id(id: int, db: Session):
  try:
    return db.query(News).filter(News.id_news == id).first()
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# CREATE
def create(data: CreateNewsDTO, db: Session):
  try:
    new_item = News(**data.model_dump())
    
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
# UPDATE
def update(id: int, data: UpdateNewsDTO, db: Session):
  try:
    item = db.query(News).filter(News.id_news == id).first()

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
  
# -----------------------------------------------------------------  
# DELETE
def delete(id: int, db: Session):
  try:
    item = db.query(News).filter(News.id_news == id).first()
    
    if not item:
      return 0

    if item.images:
      raise ValueError("No se puede eliminar la noticia porque tiene imágenes asociadas")

    db.delete(item)
    db.commit()
    return 1 
  except IntegrityError as e:
    db.rollback()
    raise ValueError("Error de integridad en la base de datos")  
  except SQLAlchemyError as e:
    db.rollback()
    raise e  
