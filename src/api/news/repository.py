from math import ceil
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models, dtos

# -----------------------------------------------------------------
# GET ALL Pagination
def get_all_pagination(
  pagination: PaginationRequestDTO, 
  db: Session
) -> PaginationResponseDTO:
  try:
    query = (
      db.query(models.News)
      .options(joinedload(models.News.images))
    )
    
    if pagination.search:
      query = query.filter(
        or_(
          models.News.title.ilike(f"%{pagination.search}%"),
          models.News.subtitle.ilike(f"%{pagination.search}%")
        )
      )
    
    items = query.count()
    pages = ceil(items / pagination.limit) if items > 0 else 0

    # Ajuste seguro de página
    page = min(pagination.page, pages) if pages > 0 else 1
    skip = (page - 1) * pagination.limit

    result = (
      query
      .order_by(models.News.created_at.asc()) # deberia ser desc
      .offset(skip)
      .limit(pagination.limit)
      .all()
    )

    return PaginationResponseDTO(
      page=page,
      pages=pages,
      items=items,
      result=result
    )
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# GET BY ID    
def get_by_id(id: int, db: Session):
  try:
    return db.query(models.News).filter(models.News.id_news == id).first()
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# CREATE
def create(data: dtos.CreateNewsDTO, db: Session):
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

# -----------------------------------------------------------------
# UPDATE
def update(id: int, data: dtos.UpdateNewsDTO, db: Session):
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
  
# -----------------------------------------------------------------  
# DELETE
def delete(id: int, db: Session):
  try:
    item = db.query(models.News).filter(models.News.id_news == id).first()
    
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
