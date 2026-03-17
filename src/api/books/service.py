from math import ceil
from typing import List
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationResponseDTO, BookPaginationRequestDTO
from src.api.editions import models as edition_models
from src.api.editorials import models as editorial_models
from src.api.books import models as book_models
from src.api.book_authors import models as book_authors_models
from . import dtos, models, repository


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(pagination: BookPaginationRequestDTO, db: Session) -> PaginationResponseDTO[List[dtos.BookDetailDTO]]:
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

  if pagination.id_editorial:
    editions = editions.filter(
      models.Edition.editorial.has(
        editorial_models.Editorial.id_editorial == pagination.id_editorial
      )
    )

  if pagination.id_author:
    editions = editions.filter(
      models.Edition.book.has(
        book_models.Book.book_authors.any(
          book_authors_models.Author.id_author == pagination.id_author
        )
      )
    )

  if pagination.id_genre:
    editions = editions.filter(
      models.Edition.book.has(
        book_models.Book.genre_id == pagination.id_genre
      )
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
    result=books_dto
  )


# -----------------------------------------------------------------
# GET BY ID
def get_book_by_id(id: int, db: Session) -> dtos.BookDetailDTO | None:
  item = repository.get_by_id(id, db)
  return dtos.BookDetailDTO.model_validate(item)


# -----------------------------------------------------------------
# CREATE
def create_book(data: dtos.CreateBookDTO, db: Session) -> dtos.BookDTO:
  item = repository.create(data, db)
  return dtos.BookDTO.model_validate(item)


# -----------------------------------------------------------------
# UPDATE
def update_book(data: dtos.UpdateBookDTO, db: Session) -> dtos.BookDTO | None:
  item = repository.update(data, db)
  return dtos.BookDTO.model_validate(item)


# -----------------------------------------------------------------
# DELETE
def delete_book(id: int, db: Session) -> bool:
  return repository.delete(id, db)

