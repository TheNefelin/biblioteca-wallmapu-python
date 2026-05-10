from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO, BookFilterDTO
from src.services import cloudinary_service
from . import dtos, repository


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO[BookFilterDTO]) -> PaginationResponseDTO[list[dtos.EditionDetailDTO]]:
  pagination_response = repository.get_all_pagination(db, pagination)
  editions = pagination_response.data or []

  data = [dtos.EditionDetailDTO.model_validate(e) for e in editions]

  return PaginationResponseDTO[list[dtos.EditionDetailDTO]](
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
    next=pagination_response.next,
    prev=pagination_response.prev,
  )


# -----------------------------------------------------------------
# GET ALL (para selects)
def get_all_editions(db: Session) -> list[dtos.EditionDetailDTO]:
  editions = repository.get_all(db)
  return [dtos.EditionDetailDTO.model_validate(e) for e in editions]


# -----------------------------------------------------------------
# GET DETAIL BY ID
def get_edition_detail_by_id(db: Session, id: int) -> dtos.EditionDetailDTO | None:
  edition = repository.get_detail_by_id(db, id)
  if not edition:
    return None
  return dtos.EditionDetailDTO.model_validate(edition)


# -----------------------------------------------------------------
# GET BY ID (básico)
def get_edition_by_id(db: Session, id: int) -> dtos.EditionDTO | None:
  edition = repository.get_entity_by_id(db, id)
  if not edition:
    return None
  return dtos.EditionDTO.model_validate(edition)


# -----------------------------------------------------------------
# CREATE
def create_edition(db: Session, data: dtos.CreateEditionDTO) -> dtos.EditionDTO:
  created = repository.create(db, data.model_dump())
  return dtos.EditionDTO.model_validate(created)


# -----------------------------------------------------------------
# UPDATE
def update_edition(db: Session, id: int, data: dtos.UpdateEditionDTO) -> dtos.EditionDTO | None:
  edition = repository.get_entity_by_id(db, id)
  if not edition:
    return None
  updated = repository.update(db, edition, data.model_dump(exclude_unset=True))
  return dtos.EditionDTO.model_validate(updated)


# -----------------------------------------------------------------
# DELETE
def delete_edition_with_image(db: Session, id: int) -> bool:
  edition = repository.get_entity_by_id(db, id)
  if not edition:
    return False

  url = repository.delete(db, edition)

  if url:
    public_id = cloudinary_service.extract_public_id(url)
    cloudinary_service.delete_image(public_id)

  return True
