from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO, BookFilterDTO
from src.services import cloudinary_service
from . import dtos, repository


# -----------------------------------------------------------------
# GET ALL PAGINATION REAL (flat DTO)
def get_all_pagination(db: Session, pagination: PaginationRequestDTO[BookFilterDTO]) -> PaginationResponseDTO[list[dtos.EditionDetailDTO]]:
  response = repository.get_all_pagination(db, pagination)
  editions = response.data or []
  data = [dtos.EditionDetailDTO.model_validate(item) for item in (editions)]

  return PaginationResponseDTO[list[dtos.EditionDetailDTO]](
    page=response.page,
    pages=response.pages,
    items=response.items,
    data=data,
    next=response.next,
    prev=response.prev,
  )


# -----------------------------------------------------------------
# GET BY BOOK ID DETAIL (flat DTO)
def get_all_by_book_id_detail(db: Session, book_id: int) -> list[dtos.EditionDetailDTO]:
  rows = repository.get_by_book_id_detail(db, book_id)
  return [dtos.EditionDetailDTO.model_validate(dict(row._mapping)) for row in (rows or [])]


# -----------------------------------------------------------------
# GET BY BOOK ID (básico)
def get_by_book_id(db: Session, book_id: int) -> list[dtos.EditionDTO]:
  editions = repository.get_by_book_id(db, book_id)
  return [dtos.EditionDTO.model_validate(e) for e in editions]


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

  if repository.has_copies(db, edition.id_edition):
    raise ValueError(f"La edición ({edition.edition}) tiene copias asociadas")

  url = repository.delete(db, edition)

  if url:
    public_id = cloudinary_service.extract_public_id(url)
    cloudinary_service.delete_image(public_id)

  return True
