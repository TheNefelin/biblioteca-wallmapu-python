from math import ceil
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from src.api.book_authors_step import repository as book_author_repo
from src.api.book_subjects_step import repository as book_subject_repo
from src.api.book_authors_step.models import BookAuthor
from src.api.book_subjects_step.models import BookSubject
from src.api.editions.models import Edition
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
        joinedload(models.Book.book_authors).joinedload(BookAuthor.author),
        joinedload(models.Book.book_subjects).joinedload(BookSubject.subject),
        joinedload(models.Book.editions),
      )
    )    

    if pagination.search:
      query = query.filter(
        or_(
          models.Book.title.ilike(f"%{pagination.search}%"),
          models.Book.editions.any(
            Edition.edition.ilike(f"%{pagination.search}%")
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
      .order_by(models.Book.updated_at.desc())
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
        joinedload(models.Book.book_authors).joinedload(BookAuthor.author),
        joinedload(models.Book.book_subjects).joinedload(BookSubject.subject),
        joinedload(models.Book.editions),
      )
      .first()
    )

    if not entity:
      return None

    return dtos.BookDTO.model_validate(entity)  
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# CREATE
def create(bookDto: dtos.CreateBookDTO, db: Session) -> dtos.BookDTO:
  try:
    # 1️⃣ Extraer datos del DTO
    new_data = bookDto.model_dump(exclude_unset=True)
    author_ids = new_data.pop("authors", None)
    subject_ids = new_data.pop("subjects", None)

    # 2️⃣ Crear la instancia de SQLAlchemy
    book = models.Book(**new_data)

    # 3️⃣ Agregar a la sesión y hacer commit
    db.add(book)
    db.commit()
    db.refresh(book)  # Para que book tenga id_book y timestamps

    # 4️⃣ Manejar relaciones con autores y subjects
    if author_ids is not None:
      book_author_repo.update(book.id_book, author_ids, db)

    if subject_ids is not None:
      book_subject_repo.update(book.id_book, subject_ids, db)

    # 5️⃣ Refrescar para incluir relaciones y devolver DTO
    db.refresh(book)
    return dtos.BookDTO.model_validate(book)
  except IntegrityError as e:
    db.rollback()
    raise ValueError(e.orig)
  except SQLAlchemyError as e:
    db.rollback()
    raise e

# -----------------------------------------------------------------
# UPDATE
def update(bookDto: dtos.UpdateBookDTO, db: Session) -> dtos.BookDTO:
  try:
    book = db.get(models.Book, bookDto.id_book)

    if not book:
      return None

    update_data = bookDto.model_dump(exclude_unset=True)
    author_ids = update_data.pop("authors", None)
    subject_ids = update_data.pop("subjects", None)

    for key, value in update_data.items():
      setattr(book, key, value)

    db.commit()

    if author_ids is not None:
      book_author_repo.update(book.id_book, author_ids, db)

    if subject_ids is not None:
      book_subject_repo.update(book.id_book, subject_ids, db)

    db.refresh(book)

    return dtos.BookDTO.model_validate(book)
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

    # 🔎 Validar dependencias usando EXISTS (más eficiente)
    has_authors = db.query(BookAuthor).filter(BookAuthor.id_book == id).first()
    if has_authors:
      raise ValueError("El libro tiene autores asociados")

    has_subjects = db.query(BookSubject).filter(BookSubject.id_book == id).first()
    if has_subjects:
      raise ValueError("El libro tiene descriptores asociados")

    has_editions = db.query(Edition).filter(Edition.book_id == id).first()
    if has_editions:
      raise ValueError("El libro tiene ediciones/ejemplares asociados")

    db.delete(book)
    db.commit()

    return True
  except SQLAlchemyError as e:
    db.rollback()
    raise e