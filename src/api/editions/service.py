from math import ceil
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload, selectinload

from src.shared.dtos import BookPaginationRequestDTO, PaginationResponseDTO
from src.services import cloudinary_service
from . import dtos, models, repository


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(pagination: BookPaginationRequestDTO, db: Session):
  query = repository.get_all_paginated(db, pagination)

  #total_items = query.count()
  total_items = db.query(models.Edition).count()

  total_pages = ceil(total_items / pagination.limit) if total_items > 0 else 0
  this_page = min(pagination.page, total_pages) if total_pages > 0 else 1
  offset = (this_page - 1) * pagination.limit

  editions = (
    query
    .options(
      joinedload(models.Edition.editorial),
      joinedload(models.Edition.book),
      selectinload(models.Edition.copies),
    )
    .order_by(models.Edition.updated_at.desc())
    .offset(offset)
    .limit(pagination.limit)
    .all()
  )

  print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))

  editions_dto = [dtos.EditionDetailDTO.model_validate(e) for e in editions]

  return PaginationResponseDTO(
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
