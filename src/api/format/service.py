from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import dtos, repository


# -----------------------------------------------------------------#
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.FormatDTO]]:
  pagination_response = repository.get_all_pagination(db, pagination)
  items = pagination_response.data or []
  
  data = [dtos.FormatDTO.model_validate(item) for item in items]

  return PaginationResponseDTO[list[dtos.FormatDTO]](
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
  )


# -----------------------------------------------------------------#
# GET ALL
def get_all(db: Session) -> list[dtos.FormatDTO]:
  items = repository.get_all(db)
  return [dtos.FormatDTO.model_validate(item) for item in items]


# -----------------------------------------------------------------#
# CREATE
def create(db: Session, dto: dtos.CreateFormatDTO) -> dtos.FormatDTO | None:
  if repository.get_by_name(db, dto.name):
    raise ValueError(f"Ya existe un formato con el nombre '{dto.name}'")

  created = repository.create(db, dto.model_dump(exclude_unset=True))
  
  if not created or not created.id_format:
    raise ValueError("Error al crear el Formato")
  
  return dtos.FormatDTO.model_validate(created)


# -----------------------------------------------------------------#
# UPDATE
def update(db: Session, id: int, dto: dtos.UpdateFormatDTO) -> dtos.FormatDTO | None:
  if dto.id_format and dto.id_format != id:
    raise ValueError(f"ID de ruta ({id}) no coincide con ID del body ({dto.id_format})")

  existing = repository.get_by_name(db, dto.name)
  if existing and existing.id_format != id:
    raise ValueError(f"Ya existe un formato con el nombre '{dto.name}'")

  updated = repository.update(db, id, dto.model_dump(exclude_unset=True))
  
  if not updated:
    return None
  
  return dtos.FormatDTO.model_validate(updated)


# -----------------------------------------------------------------#
# DELETE
def delete(db: Session, id: int) -> bool | None:
  return repository.delete(db, id)
