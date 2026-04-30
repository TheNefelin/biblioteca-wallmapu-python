from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import dtos, repository


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.GenreDTO]]:
  try:
    pagination_response = repository.get_all_pagination(db, pagination)
    items = pagination_response.data or []
    
    data = [dtos.GenreDTO.model_validate(item) for item in items]

    return PaginationResponseDTO[list[dtos.GenreDTO]](
      page=pagination_response.page,
      pages=pagination_response.pages,
      items=pagination_response.items,
      data=data,
      next=pagination_response.next,
      prev=pagination_response.prev,
    )
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.GenreDTO]:
  try:
    items = repository.get_all(db)
    return [dtos.GenreDTO.model_validate(item) for item in items]
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# CREATE
def create(db: Session, dto: dtos.CreateGenreDTO) -> dtos.GenreDTO | None:
  try:
    created = repository.create(db, dto.model_dump(exclude_unset=True))

    if not created or not created.id_genre:
      raise ValueError("Error al crear el Genero")

    return dtos.GenreDTO.model_validate(created)
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, id: int, dto: dtos.UpdateGenreDTO) -> dtos.GenreDTO | None:
  try:
    if dto.id_genre and dto.id_genre != id:
      raise ValueError(f"ID de ruta ({id}) no coincide con ID del body ({dto.id_genre})")
    
    updated = repository.update(db, id, dto.model_dump(exclude_unset=True))
    
    if not updated:
      return None
    
    return dtos.GenreDTO.model_validate(updated)
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, id: int) -> bool | None:
  try:
    return repository.delete(db, id)
  except Exception as e:
    raise e

