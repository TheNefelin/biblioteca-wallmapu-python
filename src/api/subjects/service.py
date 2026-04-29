from sqlalchemy.orm import Session

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO

from . import dtos, repository


# -----------------------------------------------------------------
# GET ALL PAGINATION
def get_all_pagination(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.SubjectDTO]]:
  try:
    pagination_response = repository.get_all_pagination(db, pagination)
    items = pagination_response.data or []
    
    data = [dtos.SubjectDTO.model_validate(item) for item in items]

    return PaginationResponseDTO[list[dtos.SubjectDTO]](
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
def get_all(db: Session) -> list[dtos.SubjectDTO]:
  try:
    items = repository.get_all(db)
    return [dtos.SubjectDTO.model_validate(item) for item in items]
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# CREATE
def create(db: Session, dto: dtos.CreateSubjectDTO) -> dtos.SubjectDTO | None:
  try:
    created = repository.create(db, dto.model_dump(exclude_unset=True))

    if not created or not created.id_subject:
      raise ValueError("Error al crear el Descriptor")

    return dtos.SubjectDTO.model_validate(created)
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, id: int, dto: dtos.UpdateSubjectDTO) -> dtos.SubjectDTO | None:
  try:
    if dto.id_subject and dto.id_subject != id:
      raise ValueError(f"ID de ruta ({id}) no coincide con ID del body ({dto.id_subject})")
    
    updated = repository.update(db, id, dto.model_dump(exclude_unset=True))
    
    if not updated:
      return None
    
    return dtos.SubjectDTO.model_validate(updated)
  except Exception as e:
    raise e


# -----------------------------------------------------------------
# DELETE
def delete(db: Session, id: int) -> bool | None:
  try:
    return repository.delete(db, id)
  except Exception as e:
    raise e

