from sqlalchemy.orm import Session
from sqlalchemy import UUID

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import dtos, repository


def get_all_detailed(pagination: PaginationRequestDTO, db: Session) -> PaginationResponseDTO[list[dtos.UserDetailDTO]]:
  page = repository.get_all_detailed(pagination, db)
  
  return PaginationResponseDTO[list[dtos.UserDetailDTO]](
    page=page.page,
    pages=page.pages,
    items=page.items,
    data=[dtos.UserDetailDTO.model_validate(item) for item in page.data],
    next=page.next,
    prev=page.prev,
  )


def get_by_id_detailed(id_user: UUID, db: Session) -> dtos.UserDetailDTO | None:
  entity = repository.get_by_id_detailed(id_user, db)
  if not entity:
    return None
  return dtos.UserDetailDTO.model_validate(entity)


def get_or_create_user(email: str, name: str, db: Session) -> dtos.UserWithRoleDTO:
  entity = repository.get_or_create_user(email, name, db)
  return dtos.UserWithRoleDTO.model_validate(entity)


def update(id_user: UUID, update_dto: dtos.UpdateUserDTO | dtos.UpdateUserByAdminDTO, db: Session) -> dtos.UserDTO | None:
  entity = repository.update(id_user, update_dto.model_dump(exclude_unset=True), db)
  if not entity:
    return None
  return dtos.UserDTO.model_validate(entity)

