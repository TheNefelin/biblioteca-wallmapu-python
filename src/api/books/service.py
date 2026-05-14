from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.api.book_authors import repository as book_authors_repository
from src.api.book_authors import service as book_author_service
from src.api.book_subjects import repository as book_subjects_repository
from src.api.book_subjects import service as book_subject_service
from . import dtos, repository


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.BookDetailDTO]]:
  response = repository.get_all_pagination(db, pagination)
  books = response.data or []
  data = [dtos.BookDetailDTO.model_validate(dict(row._mapping)) for row in books]

  return PaginationResponseDTO[list[dtos.BookDetailDTO]](
    page=response.page,
    pages=response.pages,
    items=response.items,
    data=data,
    next=response.next,
    prev=response.prev,
  )


# -----------------------------------------------------------------
# GET BY ID
def get_book_by_id(db: Session, id: int) -> dtos.BookDTO | None:
  item = repository.get_by_id(db, id)
  if not item:
    return None
  return dtos.BookDTO.model_validate(item)


# -----------------------------------------------------------------
# CREATE
def create_book(db: Session, data: dtos.CreateBookDTO) -> dtos.BookDTO:
  dump = data.model_dump(exclude_unset=True)
  author_ids = dump.pop("author_ids", []) or []
  subject_ids = dump.pop("subject_ids", []) or []

  if dump.get("genre_id") == 0:
    raise ValueError("El género es requerido")

  try:
    book = repository.create(db, dump)
    book_author_service.update_authors(db, book.id_book, author_ids)
    book_subject_service.update_subjects(db, book.id_book, subject_ids)
    db.refresh(book)
    return dtos.BookDTO.model_validate(book)
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)


# -----------------------------------------------------------------
# UPDATE
def update_book(db: Session, data: dtos.UpdateBookDTO) -> dtos.BookDTO | None:
  book = repository.get_entity_by_id(db, data.id_book)
  if not book:
    return None

  dump = data.model_dump(exclude_unset=True)
  author_ids = dump.pop("author_ids", []) or []
  subject_ids = dump.pop("subject_ids", []) or []
  dump.pop("id_book", None)

  if dump.get("genre_id") == 0:
    raise ValueError("El género es requerido")

  try:
    book = repository.update(db, book, dump)
    book_author_service.update_authors(db, book.id_book, author_ids)
    book_subject_service.update_subjects(db, book.id_book, subject_ids)
    db.refresh(book)
    return dtos.BookDTO.model_validate(book)
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)


# -----------------------------------------------------------------
# DELETE
def delete_book(db: Session, id: int) -> bool:
  from src.api.reservations import repository as reservations_repository
  from src.api.loans import repository as loans_repository

  book = repository.get_entity_by_id(db, id)
  if not book:
    return False

  if repository.has_authors(db, id):
    raise ValueError("El libro tiene autores asociados")
  if repository.has_subjects(db, id):
    raise ValueError("El libro tiene descriptores asociados")
  if repository.has_editions(db, id):
    raise ValueError("El libro tiene ediciones/ejemplares asociados")

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
  repository.delete(db, book)
  return True

