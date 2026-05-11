from sqlalchemy.orm import Session

from src.api.copy_status import models as status_models
from src.api.editions import models as edition_models
from src.api.loans import repository as loan_repository
from src.api.reservations import repository as reservation_repository
from . import dtos, repository


# -----------------------------------------------------------------
# Helpers: availability + mapping
def _compute_availability(row, loaned_ids: set, reserved_ids: set) -> tuple[bool, str]:
  if row.status_id != 1:
    return False, row.status_name
  if row.id_copy in reserved_ids:
    return False, "Pendiente de Retiro"
  if row.id_copy in loaned_ids:
    return False, "En Préstamo"
  return True, "Disponible"


def _map_to_detail(row, loaned_ids: set, reserved_ids: set) -> dtos.CopyDetailDTO:
  available, status = _compute_availability(row, loaned_ids, reserved_ids)
  data = dict(row._mapping)
  data["is_availability"] = available
  data["availability_status"] = status
  return dtos.CopyDetailDTO.model_validate(data)


# -----------------------------------------------------------------
# GET ALL DETAIL BY EDITION ID
def get_all_detail_by_edition_id(db: Session, edition_id: int) -> list[dtos.CopyDetailDTO]:
  rows = repository.get_all_detail_by_edition_id(db, edition_id)
  loaned_ids = {l.copy_id for l in loan_repository.get_all_active(db)}
  reserved_ids = {r.copy_id for r in reservation_repository.get_all_pending(db)}
  return [_map_to_detail(r, loaned_ids, reserved_ids) for r in rows]


# -----------------------------------------------------------------
# GET ALL DETAIL BY BOOK ID
def get_all_detail_by_book_id(db: Session, book_id: int) -> list[dtos.CopyDetailDTO]:
  rows = repository.get_all_detail_by_book_id(db, book_id)
  loaned_ids = {l.copy_id for l in loan_repository.get_all_active(db)}
  reserved_ids = {r.copy_id for r in reservation_repository.get_all_pending(db)}
  return [_map_to_detail(r, loaned_ids, reserved_ids) for r in rows]


# -----------------------------------------------------------------
# CREATE COPY
def create(db: Session, data: dtos.CreateCopyDTO) -> dtos.CopyDTO:
  if not db.get(edition_models.Edition, data.edition_id):
    raise ValueError("No se encontró la edición")

  if repository.signature_exists(db, data.signature_topography):
    raise ValueError("La Firma Topográfica ya existe")

  if repository.copy_number_exists(db, data.edition_id, data.copy_number):
    raise ValueError(f"El número de ejemplar {data.copy_number} ya existe para esta edición")

  entity_data = data.model_dump()
  entity_data["barcode"] = data.signature_topography
  entity_data["status_id"] = 1

  entity = repository.create(db, entity_data)
  return dtos.CopyDTO.model_validate(entity)


# -----------------------------------------------------------------
# UPDATE COPY
def update(db: Session, id: int, data: dtos.UpdateCopyDTO) -> dtos.CopyDTO | None:
  if not db.get(edition_models.Edition, data.edition_id):
    raise ValueError("No se encontró la edición")
  if not db.get(status_models.CopyStatus, data.status_id):
    raise ValueError("No se encontró el estado")

  current = repository.get_by_id(db, id)
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

  entity = repository.update(db, current, update_data)
  return dtos.CopyDTO.model_validate(entity)


# -----------------------------------------------------------------
# DELETE COPY
def delete(db: Session, id: int) -> bool:
  item = repository.get_by_id(db, id)
  if not item:
    return False

  repository.delete(db, item)
  return True




