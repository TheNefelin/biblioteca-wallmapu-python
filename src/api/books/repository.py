from math import ceil
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models

# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(
  pagination: PaginationRequestDTO, 
  db: Session
) -> PaginationResponseDTO:
  try:
    query = db.query(models.Book)

    if pagination.search:
      query = query.filter(
        or_(
          models.Book.title.ilike(f"%{pagination.search}%"),
          models.Book.edition.ilike(f"%{pagination.search}%")
        )
      )

    items = query.count()
    pages = ceil(items / pagination.limit) if items > 0 else 0

    # Ajuste seguro de página
    page = min(pagination.page, pages) if pages > 0 else 1
    skip = (page - 1) * pagination.limit

    result = (
      query
      .order_by(models.Book.title.asc())
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

