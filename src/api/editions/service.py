from math import ceil
from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.shared.dtos import BookPaginationRequestDTO, PaginationResponseDTO
from src.services import cloudinary_service
from src.api.books import models as book_models
from src.api.book_authors import models as book_authors_models
from src.api.editorials import models as editorial_models
from . import dtos, models, repository

# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(pagination: BookPaginationRequestDTO, db: Session):
  editions = repository.get_all_pagination(db)

  if pagination.search:
    editions = editions.filter(
      or_(
        models.Edition.isbn.ilike(f"%{pagination.search}%"),
        models.Edition.book.has(
          or_(
            book_models.Book.title.ilike(f"%{pagination.search}%"),
            book_models.Book.summary.ilike(f"%{pagination.search}%"),
          )
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

  total_items = editions.count()
  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
  this_page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (this_page - 1) * pagination.limit

  edition_paginated = (
    editions
    .order_by(models.Edition.updated_at.desc())
    .offset(offset)
    .limit(pagination.limit)
    .all()
  )

  editions_dto = [dtos.EditionDetailDTO.model_validate(e) for e in edition_paginated]

  return PaginationResponseDTO[list[dtos.EditionDetailDTO]](
    page=this_page,
    pages=total_pages,
    items=total_items,
    result=editions_dto,
  )

# -----------------------------------------------------------------
# GET ALL
def get_all_editions(db: Session) -> list[dtos.EditionDetailDTO]:
  editions = repository.get_all(db)
  return [dtos.EditionDetailDTO.model_validate(e) for e in editions]


# -----------------------------------------------------------------
# GET BY ID
def get_edition_by_id(id: int, db: Session) -> dtos.EditionDetailDTO | None:
  edition = repository.get_by_id(id, db)
  if not edition:
    return None
  return dtos.EditionDetailDTO.model_validate(edition)


# -----------------------------------------------------------------
# CREATE
def create_edition(data: dtos.CreateEditionDTO, db: Session) -> dtos.EditionDTO:
  new_item = repository.create(data.model_dump(), db)
  return dtos.EditionDTO.model_validate(new_item)


# -----------------------------------------------------------------
# UPDATE
def update_edition(id: int, data: dtos.UpdateEditionDTO, db: Session) -> dtos.EditionDTO | None:
  edition = repository.get_entity_by_id(id, db)
  if not edition:
    return None
  updated = repository.update(edition, data.model_dump(exclude_unset=True), db)
  return dtos.EditionDTO.model_validate(updated)


# -----------------------------------------------------------------
# DELETE
def delete_edition_with_image(id: int, db: Session) -> bool:
  edition = repository.get_entity_by_id(id, db)
  if not edition:
    return False

  url = repository.delete(edition, db)

  if url:
    public_id = cloudinary_service.extract_public_id(url)
    cloudinary_service.delete_image(public_id)

  return True
