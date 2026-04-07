from sqlalchemy.orm import Session

from src.api.copy_status import models as status_models
from src.api.editions import models as edition_models
from src.services.signature_generator import generate_signature_topography, generate_barcode
from . import dtos, models, repository


def get_all(db: Session) -> list[dtos.CopyDTO]:
  items = repository.get_all(db)
  return [dtos.CopyDTO.model_validate(item) for item in items]


def get_by_id(id: int, db: Session) -> dtos.CopyDTO | None:
  item = repository.get_by_id(id, db)
  if not item:
    return None
  return dtos.CopyDTO.model_validate(item)


def get_by_edition_id(id_edition: int, db: Session) -> list[dtos.CopyDTO]:
  items = repository.get_by_edition_id(id_edition, db)
  return [dtos.CopyDTO.model_validate(item) for item in items]


def create(data: dtos.CreateCopyDTO, db: Session) -> dtos.CopyDTO:
  if not db.get(edition_models.Edition, data.edition_id):
    raise ValueError("No se encontro la edición")
  if not db.get(status_models.CopyStatus, data.status_id):
    raise ValueError("No se encontro el estado")

  signature = generate_signature_topography(db, data.edition_id)
  barcode = generate_barcode(db, data.edition_id)

  entity_data = data.model_dump()
  entity_data["signature_topography"] = signature
  entity_data["barcode"] = barcode

  entity = repository.create(entity_data, db)
  return dtos.CopyDTO.model_validate(entity)


def update(id: int, data: dtos.UpdateCopyDTO, db: Session) -> dtos.CopyDTO | None:
  if not db.get(edition_models.Edition, data.edition_id):
    raise ValueError("No se encontro la edición")
  if not db.get(status_models.CopyStatus, data.status_id):
    raise ValueError("No se encontro el estado")

  current = repository.get_by_id(id, db)
  if not current:
    return None

  update_data = data.model_dump(exclude_unset=True)

  if "signature_topography" in update_data and update_data["signature_topography"] is not None:
    new_signature = update_data["signature_topography"]
    if new_signature != current.signature_topography:
      if repository.signature_exists_for_other(db, new_signature, id):
        raise ValueError("La signatura topográfica ya está en uso por otro ejemplar")
      update_data["barcode"] = new_signature

  entity = repository.update(id, update_data, db)
  if not entity:
    return None
  return dtos.CopyDTO.model_validate(entity)


def delete(id: int, db: Session) -> bool:
  return repository.delete(id, db)


def get_available_by_book_id(db: Session, book_id: int) -> list[dtos.CopyDTO]:
  items = repository.get_by_book_id_and_status(db, book_id, 1)
  return [dtos.CopyDTO.model_validate(item) for item in items]


def get_all_by_book_id_with_availability(db: Session, book_id: int) -> list[dtos.CopyWithAvailabilityDTO]:
  from src.api.loans.repository import get_active_by_book_id as get_loans_by_book
  from src.api.reservations.repository import get_active_by_book_id as get_reservations_by_book

  copies = repository.get_all_by_book_id(db, book_id)

  active_loans = {loan.copy_id for loan in get_loans_by_book(db, book_id)}
  active_reservations = {res.copy_id for res in get_reservations_by_book(db, book_id)}

  result = []
  for copy in copies:
    if copy.status_id != 1:
      availability = copy.status.name
    elif copy.id_copy in active_loans:
      availability = "prestado"
    elif copy.id_copy in active_reservations:
      availability = "reservado"
    else:
      availability = "disponible"

    result.append(dtos.CopyWithAvailabilityDTO(
      id_copy=copy.id_copy,
      barcode=copy.barcode,
      signature_topography=copy.signature_topography,
      copy_number=copy.copy_number,
      edition_id=copy.edition_id,
      edition=dtos.EditionBasicDTO(
        id_edition=copy.edition.id_edition,
        edition=copy.edition.edition,
        isbn=copy.edition.isbn,
        publication_year=copy.edition.publication_year,
        pages=copy.edition.pages,
        cover_image=copy.edition.cover_image,
        editorial_id=copy.edition.editorial_id,
        editorial_name=copy.edition.editorial.name if copy.edition.editorial else None
      ),
      availability_status=availability
    ))

  return result

