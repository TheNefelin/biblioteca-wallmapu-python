from sqlalchemy.orm import Session

from src.services import cloudinary_service
from . import dtos, repository

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
