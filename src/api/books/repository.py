from math import ceil
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from src.api.book_subjects_step.models import BookSubject
from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models, dtos

# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(
  pagination: PaginationRequestDTO, 
  db: Session
) -> PaginationResponseDTO:
  try:
    query = (
      db.query(models.Book)
      .options(
        joinedload(models.Book.genre),
        joinedload(models.Book.book_authors).joinedload(models.BookAuthor.author),
        joinedload(models.Book.book_subjects).joinedload(BookSubject.subject),
        joinedload(models.Book.editions),
      )
    )    

    if pagination.search:
      query = query.filter(
        or_(
          models.Book.title.ilike(f"%{pagination.search}%"),
          models.Book.editions.any(
            models.Edition.edition.ilike(f"%{pagination.search}%")
          )
        )
      )

    items = query.count()
    pages = ceil(items / pagination.limit) if items > 0 else 0

    # Ajuste seguro de página
    page = min(pagination.page, pages) if pages > 0 else 1
    skip = (page - 1) * pagination.limit

    resultModel = (
      query
      .order_by(models.Book.title.asc())
      .offset(skip)
      .limit(pagination.limit)
      .all()
    )

    resultDto = [dtos.BookDTO.model_validate(item) for item in resultModel]

    return PaginationResponseDTO(
      page=page,
      pages=pages,
      items=items,
      result=resultDto
    )
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# GET BY ID    
def get_by_id(id: int, db: Session) -> dtos.BookDTO:
  try:
    entity = (
      db.query(models.Book)
      .filter(models.Book.id_book == id)
      .options(
        joinedload(models.Book.genre),
        joinedload(models.Book.book_authors).joinedload(models.BookAuthor.author),
        joinedload(models.Book.book_subjects).joinedload(BookSubject.subject),
        joinedload(models.Book.editions),
      )
      .first()
    )

    if not entity:
      return None

    print(entity)

    return dtos.BookDTO.model_validate(entity)  
  except SQLAlchemyError as e:
    raise e

