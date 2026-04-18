from math import ceil
from typing import List
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.api.editions import models as edition_models
from src.api.authors import models as authors_models
from src.api.book_authors import repository as book_authors_repository
from src.api.book_subjects import repository as book_subjects_repository
from . import dtos, models, repository


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(pagination: PaginationRequestDTO, db: Session) -> PaginationResponseDTO[List[dtos.BookDetailDTO]]:
  books = repository.get_all_pagination(db)

  if pagination.search:
    books = books.filter(
      or_(
        models.Book.title.ilike(f"%{pagination.search}%"),
        models.Book.summary.ilike(f"%{pagination.search}%"),
        models.Book.editions.any(
          edition_models.Edition.isbn.ilike(f"%{pagination.search}%")
        )
      )
    )

  filters = None

  if filters and filters.id_editorial:
    books = books.filter(
      models.Book.editions.any(
        edition_models.Edition.editorial_id == filters.id_editorial
      )
    )

  if filters and filters.id_author:
    books = books.filter(
      models.Book.book_authors.any(
        authors_models.Author.id_author == filters.id_author
      )
    )

  if filters and filters.id_genre:
    books = books.filter(
      models.Book.genre_id == filters.id_genre
    )

  total_items = books.count()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
  this_page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (this_page - 1) * pagination.limit

  book_paginated = (
    books
    .order_by(models.Book.updated_at.desc())
    .offset(offset)
    .limit(pagination.limit)
    .all()
  )

  books_dto = [dtos.BookDetailDTO.model_validate(item) for item in book_paginated]

  return PaginationResponseDTO[List[dtos.BookDetailDTO]](
    page=this_page,
    pages=total_pages,
    items=total_items,
    data=books_dto,
    next=None,
    prev=None
  )

# -----------------------------------------------------------------
# GET BY ID
def get_book_detail_by_id(id: int, db: Session) -> dtos.BookDetailDTO | None:
  item = repository.get_by_id(id, db)
  if not item:
    return None
  return dtos.BookDetailDTO.model_validate(item)


# -----------------------------------------------------------------
# GET BY ID
def get_book_by_id(id: int, db: Session) -> dtos.BookDTO | None:
  item = repository.get_by_id(id, db)
  if not item:
    return None
  return dtos.BookDTO.model_validate(item)


# -----------------------------------------------------------------
# CREATE
def create_book(data: dtos.CreateBookDTO, db: Session) -> dtos.BookDTO:
  item = repository.create(data.model_dump(exclude_unset=True), db)
  return dtos.BookDTO.model_validate(item)


# -----------------------------------------------------------------
# UPDATE
def update_book(data: dtos.UpdateBookDTO, db: Session) -> dtos.BookDTO | None:
  item = repository.update(data.model_dump(exclude_unset=True), db)
  return dtos.BookDTO.model_validate(item)


# -----------------------------------------------------------------
# DELETE
def delete_book(id: int, db: Session) -> bool:
  from src.api.reservations import repository as reservations_repository
  from src.api.loans import repository as loans_repository

  dependencies = []

  active_reservations = reservations_repository.get_active_by_book_id(db, id)
  if active_reservations:
    dependencies.append("reservas activas")

  active_loans = loans_repository.get_active_by_book_id(db, id)
  if active_loans:
    dependencies.append("préstamos activos")

  if dependencies:
    raise ValueError(f"No se puede eliminar el libro. Dependencias: {', '.join(dependencies)}")

  book_authors_repository.delete_by_book(id, db)
  book_subjects_repository.delete_by_book(id, db)

  result = repository.delete(id, db)
  if result is None:
    return False
  return result

