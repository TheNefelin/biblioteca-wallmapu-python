from math import ceil
from typing import List
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from src.api.book_authors import models as book_authors_model
from src.api.book_authors import service as book_author_service
from src.api.book_subjects import models as book_subjects_model
from src.api.book_subjects import service as book_subject_service
from src.api.editions import models as edition_models
from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import models, dtos


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(
  db: Session
) -> List[models.Book]:
  try:
    books = (
      db.query(models.Book)
      .options(
        joinedload(models.Book.genre),
        joinedload(models.Book.book_authors).joinedload(book_authors_model.BookAuthor.author),
        joinedload(models.Book.book_subjects).joinedload(book_subjects_model.BookSubject.subject),
        joinedload(models.Book.editions).joinedload(edition_models.Edition.copies),
      )
    )

    return books
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# GET ALL
def get_all(
  pagination: PaginationRequestDTO, 
  db: Session
) -> PaginationResponseDTO:
  try:
    query = (
      db.query(models.Book)
      .options(
        joinedload(models.Book.genre),
        joinedload(models.Book.book_authors).joinedload(book_authors_model.BookAuthor.author),
        joinedload(models.Book.book_subjects).joinedload(book_subjects_model.BookSubject.subject),
        joinedload(models.Book.editions).joinedload(edition_models.Edition.copies),
      )
    )

    if pagination.search:
      query = query.filter(
        or_(
          models.Book.title.ilike(f"%{pagination.search}%"),
          models.Book.editions.any(
            edition_models.Edition.edition.ilike(f"%{pagination.search}%")
          )
        )
      )

    items = query.count()
    pages = ceil(items / pagination.limit) if items > 0 else 0
    page = min(pagination.page, pages) if pages > 0 else 1
    skip = (page - 1) * pagination.limit

    result_model = (
      query
      .order_by(models.Book.updated_at.desc())
      .offset(skip)
      .limit(pagination.limit)
      .all()
    )

    result_dto = [dtos.BookDetailDTO.model_validate(item) for item in result_model]

    return PaginationResponseDTO(
      page=page,
      pages=pages,
      items=items,
      result=result_dto
    )
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# GET BY ID    
def get_by_id(id: int, db: Session) -> models.Book:
  try:
    entity = (
      db.query(models.Book)
      .filter(models.Book.id_book == id)
      .options(
        joinedload(models.Book.genre),
        joinedload(models.Book.book_authors).joinedload(book_authors_model.BookAuthor.author),
        joinedload(models.Book.book_subjects).joinedload(book_subjects_model.BookSubject.subject),
        joinedload(models.Book.editions).joinedload(edition_models.Edition.copies),
      )
      .first()
    )

    if not entity:
      return None

    return entity
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# CREATE
def create(bookDto: dtos.CreateBookDTO, db: Session) -> models.Book:
  try:
    # Extraer datos del DTO
    new_data = bookDto.model_dump(exclude_unset=True)
    author_ids = new_data.pop("author_ids", None)
    subject_ids = new_data.pop("subject_ids", None)
    author_ids = author_ids or []
    subject_ids = subject_ids or []

    # Crear instancia de SQLAlchemy
    book = models.Book(**new_data)
    db.add(book)
    db.commit()
    db.refresh(book)  # obtiene id_book y timestamps

    # Relación con autores y subjects (array vacío elimina todas las relaciones)
    book_author_service.update_authors(book.id_book, author_ids, db)
    book_subject_service.update_subjects(book.id_book, subject_ids, db)

    db.commit()
    db.refresh(book)

    return book
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------
# UPDATE
def update(bookDto: dtos.UpdateBookDTO, db: Session) -> models.Book:
  try:
    book = db.get(models.Book, bookDto.id_book)

    if not book:
      return None

    update_data = bookDto.model_dump(exclude_unset=True)
    update_data.pop("id_book", None)  # evitar sobrescribir PK

    for key, value in update_data.items():
      setattr(book, key, value)

    author_ids = update_data.pop("author_ids", None)
    subject_ids = update_data.pop("subject_ids", None)
    author_ids = author_ids or []
    subject_ids = subject_ids or []

    book_author_service.update_authors(book.id_book, author_ids, db)
    book_subject_service.update_subjects(book.id_book, subject_ids, db)

    db.commit()
    db.refresh(book)

    return book
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)
  except SQLAlchemyError as e:
    db.rollback()
    raise e
    
# -----------------------------------------------------------------
# DELETE
def delete(id: int, db: Session) -> bool:
  try:
    book = db.get(models.Book, id)
    
    if not book:
      return None

    # Validar dependencias
    if db.query(book_authors_model.BookAuthor).filter_by(id_book=id).first():
      raise ValueError("El libro tiene autores asociados")

    if db.query(book_subjects_model.BookSubject).filter_by(id_book=id).first():
      raise ValueError("El libro tiene descriptores asociados")

    if db.query(edition_models.Edition).filter_by(book_id=id).first():
      raise ValueError("El libro tiene ediciones/ejemplares asociados")

    db.delete(book)
    db.commit()

    return True
  except SQLAlchemyError as e:
    db.rollback()
    raise e