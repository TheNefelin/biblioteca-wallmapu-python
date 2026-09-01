from sqlalchemy.ext.asyncio import AsyncSession

from rfc9457 import BadRequestProblem
from src.core.exceptions import NotFoundError
from src.models import models
from src.api.loans import repository as loan_repository
from src.api.reservations import repository as reservation_repository
from src.schemas.dtos import CopyDTO, CopyDetailDTO, CreateCopyDTO, UpdateCopyDTO
from . import repository


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


def _map_to_detail(row, loaned_ids: set, reserved_ids: set) -> CopyDetailDTO:
  available, status = _compute_availability(row, loaned_ids, reserved_ids)
  data = dict(row._mapping)
  data["is_availability"] = available
  data["availability_status"] = status
  return CopyDetailDTO.model_validate(data)


# -----------------------------------------------------------------
# GET ALL DETAIL BY EDITION ID
async def get_all_detail_by_edition_id(db: AsyncSession, edition_id: int) -> list[CopyDetailDTO]:
  rows = await repository.get_all_detail_by_edition_id(db, edition_id)
  loaned_ids = {l.copy_id for l in await loan_repository.get_all_active(db)}
  reserved_ids = {r.copy_id for r in await reservation_repository.get_all_pending(db)}
  return [_map_to_detail(r, loaned_ids, reserved_ids) for r in rows]


# -----------------------------------------------------------------
# GET ALL DETAIL BY BOOK ID
async def get_all_detail_by_book_id(db: AsyncSession, book_id: int) -> list[CopyDetailDTO]:
  rows = await repository.get_all_detail_by_book_id(db, book_id)
  rows = [r for r in rows if r.status_id == 1]
  loaned_ids = {l.copy_id for l in await loan_repository.get_all_active(db)}
  reserved_ids = {r.copy_id for r in await reservation_repository.get_all_pending(db)}
  return [_map_to_detail(r, loaned_ids, reserved_ids) for r in rows]


# -----------------------------------------------------------------
# CREATE COPY
async def create(db: AsyncSession, data: CreateCopyDTO) -> CopyDTO:
  edition = await db.get(models.Edition, data.edition_id)
  if not edition:
    raise NotFoundError(entity="Edición")

  if await repository.signature_exists(db, data.signature_topography):
    raise BadRequestProblem(detail="La Firma Topográfica ya existe")

  if await repository.copy_number_exists(db, data.edition_id, data.copy_number):
    raise BadRequestProblem(detail=f"El número de ejemplar {data.copy_number} ya existe para esta edición")

  entity_data = data.model_dump()
  entity_data["barcode"] = data.signature_topography
  entity_data["status_id"] = 1

  entity = await repository.create(db, entity_data)
  return CopyDTO.model_validate(entity)


# -----------------------------------------------------------------
# UPDATE COPY
async def update(db: AsyncSession, id: int, data: UpdateCopyDTO) -> CopyDTO | None:
  if data.id_copy != id:
    raise BadRequestProblem(detail="El ID no coincide")

  edition = await db.get(models.Edition, data.edition_id)
  if not edition:
    raise NotFoundError(entity="Edición")
  status = await db.get(models.CopyStatus, data.status_id)
  if not status:
    raise NotFoundError(entity="Estado")

  current = await repository.get_by_id(db, id)
  if not current:
    return None

  update_data = data.model_dump(exclude_unset=True)

  if "signature_topography" in update_data and update_data["signature_topography"] is not None:
    new_signature = update_data["signature_topography"]
    if new_signature != current.signature_topography:
      if await repository.signature_exists(db, new_signature, exclude_id=id):
        raise BadRequestProblem(detail="La signatura topográfica ya está en uso por otro ejemplar")
      update_data["barcode"] = new_signature

  if "copy_number" in update_data and update_data["copy_number"] is not None:
    new_copy_number = update_data["copy_number"]
    if new_copy_number != current.copy_number:
      if await repository.copy_number_exists(db, data.edition_id, new_copy_number, exclude_id=id):
        raise BadRequestProblem(detail=f"El número de ejemplar {new_copy_number} ya existe para esta edición")

  entity = await repository.update(db, current, update_data)
  return CopyDTO.model_validate(entity)


# -----------------------------------------------------------------
# DELETE COPY
async def delete(db: AsyncSession, id: int) -> bool:
  item = await repository.get_by_id(db, id)
  if not item:
    return False

  if await loan_repository.exists_by_copy_id(db, id):
    raise BadRequestProblem(detail="No se puede eliminar el ejemplar porque tiene préstamos asociados")

  if await reservation_repository.exists_by_copy_id(db, id):
    raise BadRequestProblem(detail="No se puede eliminar el ejemplar porque tiene reservas asociadas")

  await repository.delete(db, item)
  return True