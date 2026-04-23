from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload, selectinload

from src.shared.dtos import PaginationRequestDTO, BookFilterDTO
from src.api.editorials import models as editorial_models
from src.api.books import models as book_models
from src.api.authors import models as authors_models
from src.api.book_authors import models as book_authors_models
from src.api.copy import models as copy_models
from . import models


# -----------------------------------------------------------------
def count_query(query):
  return query.with_entities(models.Edition.id_edition).distinct().count()

def get_paginated(query, offset: int, limit: int):
  return (
    query
    .options(
      joinedload(models.Edition.editorial),
      joinedload(models.Edition.book),
      selectinload(models.Edition.copies),
    )
    .order_by(models.Edition.updated_at.desc())
    .offset(offset)
    .limit(limit)
    .all()
  )
  
def build_query(pagination: PaginationRequestDTO[BookFilterDTO], db: Session):
  query = db.query(models.Edition)

  query = query.join(models.Edition.book)

  if pagination.search:
    query = query.filter(
      or_(
        models.Edition.isbn.ilike(f"%{pagination.search}%"),
        book_models.Book.title.ilike(f"%{pagination.search}%"),
        book_models.Book.summary.ilike(f"%{pagination.search}%"),
      )
    )

  if pagination.filter:
    if pagination.filter.id_author:
      query = (
        query.join(book_models.Book.book_authors)
          .join(book_authors_models.BookAuthor.author)
          .filter(authors_models.Author.id_author == pagination.filter.id_author)
      )

    if pagination.filter.id_editorial:
      query = query.filter(
        models.Edition.editorial_id == pagination.filter.id_editorial
      )

    if pagination.filter.id_genre:
      query = query.filter(
        book_models.Book.genre_id == pagination.filter.id_genre
      )

  return query
  
# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_paginated(
  pagination,
  db: Session,
):
  query = db.query(models.Edition)

  # -------------------------
  # JOINS dinámicos
  # -------------------------
  query = query.join(models.Edition.book)

  # -------------------------
  # FILTROS
  # -------------------------
  if pagination.search:
    query = query.filter(
      or_(
        models.Edition.isbn.ilike(f"%{pagination.search}%"),
        book_models.Book.title.ilike(f"%{pagination.search}%"),
        book_models.Book.summary.ilike(f"%{pagination.search}%"),
      )
    )

  if pagination.id_editorial:
    query = query.filter(
      editorial_models.Editorial.id_editorial == pagination.id_editorial
    )

  if pagination.id_author:
    query = query.join(book_models.Book.book_authors).join(book_authors_models.BookAuthor.author)
    query = query.filter(book_authors_models.Author.id_author == pagination.id_author)

  if pagination.id_genre:
    query = query.filter(
      book_models.Book.genre_id == pagination.id_genre
    )

  return query.distinct()
 

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Edition]:
  stmt = (
    select(models.Edition)
    .options(
      joinedload(models.Edition.editorial),
      joinedload(models.Edition.book),
      joinedload(models.Edition.copies),
    )
    .order_by(models.Edition.edition.asc())
  )

  #return db.scalars(stmt).all()
  return db.scalars(stmt).unique().all()


# -----------------------------------------------------------------
# GET BY ID
def get_detail_by_id(id: int, db: Session) -> models.Edition | None:
  stmt = (
    select(models.Edition)
    .options(
      joinedload(models.Edition.editorial),
      joinedload(models.Edition.book),
      joinedload(models.Edition.copies),
    )
    .where(models.Edition.id_edition == id)
  )

  return db.scalars(stmt).first()


# -----------------------------------------------------------------
# GET ENTITY BY ID (sin joins)
def get_entity_by_id(id: int, db: Session) -> models.Edition | None:
  return db.get(models.Edition, id)


# -----------------------------------------------------------------
# CREATE
def create(data: dict, db: Session) -> models.Edition:
  try:
    new_item = models.Edition(**data)
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item
  except IntegrityError as e:
    db.rollback()
    raise ValueError(f"Violación de integridad: {e.orig}")
  except SQLAlchemyError as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# UPDATE
def update(item: models.Edition, data: dict, db: Session) -> models.Edition:
  try:
    for key, value in data.items():
      setattr(item, key, value)
    
    db.commit()
    db.refresh(item)

    return item
  except IntegrityError as e:
    db.rollback()
    raise ValueError(f"Violación de integridad: {e.orig}")
  except SQLAlchemyError as e:
    db.rollback()
    raise e


# -----------------------------------------------------------------
# DELETE
def delete(edition: models.Edition, db: Session) -> str | None:
  try:
    # Validar dependencias
    has_copies = (
      db.query(copy_models.Copy)
      .filter(copy_models.Copy.edition_id == edition.id_edition)
      .first()
    )
    if has_copies:
      raise ValueError(f"El Ejemplar ({edition.edition}) tiene copias asociados")

    url = edition.cover_image
    db.delete(edition)
    db.commit()
    
    return url
  except SQLAlchemyError as e:
    db.rollback()
    raise e
