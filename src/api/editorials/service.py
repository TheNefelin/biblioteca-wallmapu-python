from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import dtos, repository


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.EditorialDTO]]:
  pagination_response = repository.get_all_pagination(db, pagination)
  items = pagination_response.data or []

  data = [dtos.EditorialDTO.model_validate(item) for item in items]

  return PaginationResponseDTO[list[dtos.EditorialDTO]](
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
  )


# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.EditorialDTO]:
  items = repository.get_all(db)
  return [dtos.EditorialDTO.model_validate(item) for item in items]


# -----------------------------------------------------------------
# GET BY ID
def get_by_id(db: Session, id: int) -> dtos.EditorialDTO | None:
  item = repository.get_by_id(db, id)
  if not item:
    return None
  return dtos.EditorialDTO.model_validate(item)


# -----------------------------------------------------------------
# CREATE
def create(db: Session, dto: dtos.CreateEditorialDTO) -> dtos.EditorialDTO:
  if repository.exists_by_name(db, dto.name):
    raise ValueError("La editorial ya existe")

  data = dto.model_dump()

  entity = repository.create(db, data)
  return dtos.EditorialDTO.model_validate(entity)


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, id: int, dto: dtos.UpdateEditorialDTO) -> dtos.EditorialDTO | None:
  if not repository.exists_by_id(db, id):
    return None

  if repository.exists_by_name(db, dto.name, exclude_id=id):
    raise ValueError("El nombre de la editorial ya está en uso")

  current = repository.get_by_id(db, id)
  update_data = dto.model_dump(exclude={"id_editorial"})

  entity = repository.update(db, current, update_data)
  return dtos.EditorialDTO.model_validate(entity)


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, id: int) -> bool | None:
  if not repository.exists_by_id(db, id):
    return None

  current = repository.get_by_id(db, id)
  repository.delete(db, current)
  return True