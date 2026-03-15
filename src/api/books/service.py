from math import ceil
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import dtos, repository


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

