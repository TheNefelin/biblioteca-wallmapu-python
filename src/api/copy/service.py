from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.api.copy_status import models as status_models
from src.api.editions import models as edition_models
from src.api.loans import repository as loan_repository
from src.api.reservations import repository as reservation_repository
from . import dtos, repository, schema


# -----------------------------------------------------------------
# GET ALL COPIES
def get_all(db: Session) -> list[dtos.CopyWithStatusDTO]:
  items = repository.get_all(db)
  return [dtos.CopyWithStatusDTO.model_validate(item) for item in items]


# -----------------------------------------------------------------
# GET COPY BY ID
def get_by_id(id: int, db: Session) -> dtos.CopyWithStatusDTO | None:
  item = repository.get_by_id(id, db)
  if not item:
    return None
  return dtos.CopyWithStatusDTO.model_validate(item)


# -----------------------------------------------------------------
# GET ALL COPIES BY EDITION ID
def get_by_edition_id(id_edition: int, db: Session) -> list[dtos.CopyWithStatusDTO]:
  items = repository.get_by_edition_id(id_edition, db)
  return [dtos.CopyWithStatusDTO.model_validate(item) for item in items]


# -----------------------------------------------------------------
# CREATE COPY
def create(data: dtos.CreateCopyDTO, db: Session) -> dtos.CopyDTO:
  if not db.get(edition_models.Edition, data.edition_id):
    raise ValueError("No se encontró la edición")

  if repository.signature_exists(db, data.signature_topography):
    raise ValueError("La Firma Topográfica ya existe")

  if repository.copy_number_exists(db, data.edition_id, data.copy_number):
    raise ValueError(f"El número de ejemplar {data.copy_number} ya existe para esta edición")

  try:
    entity_data = data.model_dump()
    entity_data["barcode"] = data.signature_topography
    entity_data["status_id"] = 1

    entity = repository.create(entity_data, db)
    return dtos.CopyDTO.model_validate(entity)
  except SQLAlchemyError:
    raise ValueError("Error al crear el ejemplar")


# -----------------------------------------------------------------
# UPDATE COPY
def update(id: int, data: dtos.UpdateCopyDTO, db: Session) -> dtos.CopyDTO | None:
  if not db.get(edition_models.Edition, data.edition_id):
    raise ValueError("No se encontró la edición")
  if not db.get(status_models.CopyStatus, data.status_id):
    raise ValueError("No se encontró el estado")

  current = repository.get_by_id(id, db)
  if not current:
    return None

  update_data = data.model_dump(exclude_unset=True)

  if "signature_topography" in update_data and update_data["signature_topography"] is not None:
    new_signature = update_data["signature_topography"]
    if new_signature != current.signature_topography:
      if repository.signature_exists(db, new_signature, exclude_id=id):
        raise ValueError("La signatura topográfica ya está en uso por otro ejemplar")
      update_data["barcode"] = new_signature

  if "copy_number" in update_data and update_data["copy_number"] is not None:
    new_copy_number = update_data["copy_number"]
    if new_copy_number != current.copy_number:
      if repository.copy_number_exists(db, data.edition_id, new_copy_number, exclude_id=id):
        raise ValueError(f"El número de ejemplar {new_copy_number} ya existe para esta edición")

  entity = repository.update(id, update_data, db)
  if not entity:
    return None
  return dtos.CopyDTO.model_validate(entity)


# -----------------------------------------------------------------
# DELETE COPY
def delete(id: int, db: Session) -> bool:
  return repository.delete(id, db)


# -----------------------------------------------------------------
# GET ALL COPIES BY BOOK ID WITH AVAILABILITY
def get_all_availability_copies_by_book(db: Session, book_id: int) -> list[schema.CopyAvailabilityDTO]:
  copies = repository.get_by_book_id_and_status(db, book_id, 1)
  dtos = [schema.CopyAvailabilityDTO.model_validate(item) for item in copies]

  active_loans = loan_repository.get_active_by_book_id(db, book_id)
  active_reservations = reservation_repository.get_active_by_book_id(db, book_id)

  loans_status_map = {int(loan.copy_id): str(loan.loan_status.name) for loan in active_loans}
  reservations_status_map = {int(res.copy_id): str(res.status.name) for res in active_reservations}

  for dto in dtos:
    if dto.id_copy in loans_status_map:
      dto.availability_status = loans_status_map[dto.id_copy]
    elif dto.id_copy in reservations_status_map:
      dto.availability_status = reservations_status_map[dto.id_copy]
    else:
      dto.availability_status = "disponible"

  return dtos