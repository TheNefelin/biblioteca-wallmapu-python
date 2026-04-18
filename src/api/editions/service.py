from math import ceil
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Optional

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO, BookFilterDTO
from src.services import cloudinary_service
from . import dtos, repository


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(pagination: PaginationRequestDTO[BookFilterDTO], db: Session):
  base_query = repository.build_query(pagination, db)

  total_items = repository.count_query(base_query)

  total_pages = ceil(total_items / pagination.limit) if total_items else 0
  page = min(pagination.page, total_pages) if total_pages else 1
  offset = (page - 1) * pagination.limit

  editions = repository.get_paginated(base_query, offset, pagination.limit)

  editions_dto = [dtos.EditionDetailDTO.model_validate(e) for e in editions]

  return PaginationResponseDTO(
    page=page,
    pages=total_pages,
    items=total_items,
    data=editions_dto,
    next=None,
    prev=None,
  )
  

# -----------------------------------------------------------------
# GET ALL
def get_all_editions(db: Session) -> list[dtos.EditionDetailDTO]:
  editions = repository.get_all(db)
  return [dtos.EditionDetailDTO.model_validate(e) for e in editions]


# -----------------------------------------------------------------
# GET BY ID
def get_edition_detail_by_id(id: int, db: Session) -> dtos.EditionDetailDTO | None:
  edition = repository.get_detail_by_id(id, db)
  if not edition:
    return None
  return dtos.EditionDetailDTO.model_validate(edition)


# -----------------------------------------------------------------
# GET BY ID
def get_edition_by_id(id: int, db: Session) -> dtos.EditionDTO | None:
  edition = repository.get_entity_by_id(id, db)
  if not edition:
    return None
  return dtos.EditionDTO.model_validate(edition)

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
