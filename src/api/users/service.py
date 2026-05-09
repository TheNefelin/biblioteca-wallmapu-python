from sqlalchemy.orm import Session
from sqlalchemy import UUID
import logging

from src.shared.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.api.notifications import service as notification_service
from . import dtos, repository

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------
# MAPPER: User ORM → UserDetailDTO
def _map_user_to_detail(user) -> dtos.UserDetailDTO:
  """Convierte entidad User ORM a UserDetailDTO con nombres de relaciones resueltos"""
  return dtos.UserDetailDTO(
    **dtos.UserDTO.model_validate(user).model_dump(),
    commune_name=user.commune.name if user.commune else "",
    user_role_name=user.user_role.name if user.user_role else "",
    user_status_name=user.user_status.name if user.user_status else "",
  )


# -----------------------------------------------------------------
# GET ALL DETAILED (PAGINATED)
def get_all_detailed(db: Session, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[dtos.UserDetailDTO]]:
  """Retorna lista paginada de usuarios con datos resueltos"""
  pagination_response = repository.get_all_detailed(db, pagination)
  users = pagination_response.data or []

  data = [_map_user_to_detail(user) for user in users]

  return PaginationResponseDTO[list[dtos.UserDetailDTO]](
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
    next=pagination_response.next,
    prev=pagination_response.prev,
  )


# -----------------------------------------------------------------
# GET BY ID DETAILED
def get_by_id_detailed(db: Session, id_user: UUID) -> dtos.UserDetailDTO | None:
  """Retorna un usuario por su UUID con datos resueltos"""
  entity = repository.get_by_id_detailed(db, id_user)

  if not entity:
    return None

  return _map_user_to_detail(entity)


# -----------------------------------------------------------------
# GET OR CREATE USER (Auth)
def get_or_create_user(db: Session, dto: dtos.CreateUser) -> dtos.UserDetailDTO:
  """Obtiene usuario por email o lo crea si no existe (usado por Auth)"""
  entity, is_new = repository.get_or_create_user(db, dto.model_dump(exclude_none=True))

  if is_new:
    try:
      notification_service.create_welcome_notification(
        db=db,
        user_id=str(entity.id_user),
        user_email=entity.email,
        user_name=entity.name,
      )
    except Exception:
      logger.warning(f"Error al enviar notificación de bienvenida para user {entity.id_user}")

  return _map_user_to_detail(entity)


# -----------------------------------------------------------------
# UPDATE USER
def update(db: Session, id_user: UUID, update_dto: dtos.UpdateUserDTO | dtos.UpdateUserByAdminDTO) -> dtos.UserDTO | None:
  """Actualiza datos de un usuario. Acepta DTO de usuario o de administrador"""
  entity = repository.update(db, id_user, update_dto.model_dump(exclude_unset=True))
  if not entity:
    return None
  return dtos.UserDTO.model_validate(entity)

