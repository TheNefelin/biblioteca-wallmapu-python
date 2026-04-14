from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Query, Session, joinedload

from src.api.book_authors import models as book_authors_model
from src.api.book_authors import service as book_author_service
from src.api.book_subjects import models as book_subjects_model
from src.api.book_subjects import service as book_subject_service
from src.api.editions import models as edition_models
from src.api.copy import models as copy_model

from . import models


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(
  db: Session
) -> Query[models.Book]:
  try:
    books = (
      db.query(models.Book)
      .options(
        joinedload(models.Book.genre),
        joinedload(models.Book.book_authors).joinedload(book_authors_model.BookAuthor.author),
        joinedload(models.Book.book_subjects).joinedload(book_subjects_model.BookSubject.subject),
        joinedload(models.Book.editions).joinedload(edition_models.Edition.copies).joinedload(copy_model.Copy.status),
      )
    )

    return books
  except SQLAlchemyError as e:
    raise e


# -----------------------------------------------------------------
# GET BY ID    
def get_by_id(id: int, db: Session) -> models.Book | None:
  try:
    entity = (
      db.query(models.Book)
      .filter(models.Book.id_book == id)
      .options(
        joinedload(models.Book.genre),
        joinedload(models.Book.book_authors).joinedload(book_authors_model.BookAuthor.author),
        joinedload(models.Book.book_subjects).joinedload(book_subjects_model.BookSubject.subject),
        joinedload(models.Book.editions).joinedload(edition_models.Edition.copies).joinedload(copy_model.Copy.status),
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
def create(data: dict, db: Session) -> models.Book:
  try:
    # Extraer datos del DTO
    new_data = dict(data)
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
def update(data: dict, db: Session) -> models.Book | None:
  try:
    book_id = data.get("id_book")
    book = db.get(models.Book, book_id)

    if not book:
      return None

    update_data = dict(data)
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
def delete(id: int, db: Session) -> bool | None:
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