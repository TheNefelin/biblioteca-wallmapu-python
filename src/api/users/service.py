import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import UUID

from src.schemas.dtos import PaginationRequestDTO, PaginationResponseDTO
from src.schemas.dtos import CreateUser, UserDTO, UserDetailDTO, UpdateUserDTO, UpdateUserByAdminDTO
from src.api.notifications import service as notification_service
from . import repository

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------
# MAPPER: User ORM â†’ UserDetailDTO
def _map_user_to_detail(user) -> UserDetailDTO:
  return UserDetailDTO(
    **UserDTO.model_validate(user).model_dump(),
    commune_name=user.commune.name if user.commune else "",
    user_role_name=user.user_role.name if user.user_role else "",
    user_status_name=user.user_status.name if user.user_status else "",
  )


# -----------------------------------------------------------------
# GET ALL DETAILED (PAGINATED)
async def get_all_detailed(db: AsyncSession, pagination: PaginationRequestDTO) -> PaginationResponseDTO[list[UserDetailDTO]]:
  pagination_response = await repository.get_all_detailed(db, pagination)
  users = pagination_response.data or []

  data = [_map_user_to_detail(user) for user in users]

  return PaginationResponseDTO[list[UserDetailDTO]](
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
  )


# -----------------------------------------------------------------
# GET BY ID DETAILED
async def get_by_id_detailed(db: AsyncSession, id_user: UUID) -> UserDetailDTO | None:
  entity = await repository.get_by_id_detailed(db, id_user)
  if not entity:
    return None
  return _map_user_to_detail(entity)


# -----------------------------------------------------------------
# GET OR CREATE USER (Auth)
async def get_or_create_user(db: AsyncSession, dto: CreateUser) -> UserDetailDTO:
  entity = await repository.get_by_email(db, dto.email)

  if not entity:
    created = await repository.create(db, dto.model_dump(exclude_none=True))
    entity = await repository.get_by_id_with_role_status(db, created.id_user)

    try:
      await notification_service.create_welcome_notification(
        db=db,
        user_id=str(entity.id_user),
        user_email=entity.email,
        user_name=entity.name,
      )
    except Exception:
      logger.warning(f"Error al enviar notificaciÃ³n de bienvenida para user {entity.id_user}")

  return _map_user_to_detail(entity)


# -----------------------------------------------------------------
# UPDATE USER
async def update(db: AsyncSession, id_user: UUID, update_dto: UpdateUserDTO) -> UserDTO | None:
  entity = await repository.update(db, id_user, update_dto.model_dump(exclude_unset=True))
  if not entity:
    return None
  return UserDTO.model_validate(entity)


# -----------------------------------------------------------------
# UPDATE USER BY ADMIN
async def update_by_admin(db: AsyncSession, id_user: UUID, update_dto: UpdateUserByAdminDTO, current_user_id: str) -> UserDTO | None:
  update_data = update_dto.model_dump(exclude_unset=True)

  if str(id_user) == current_user_id:
    update_data.pop("user_role_id", None)
    update_data.pop("user_status_id", None)

  entity = await repository.update(db, id_user, update_data)
  if not entity:
    return None
  return UserDTO.model_validate(entity)


# -----------------------------------------------------------------
# GET ROLE NAME BY USER ID (para security: el rol real se lee de la BD)
async def get_role_name_by_id(db: AsyncSession, id_user: UUID) -> str | None:
  entity = await repository.get_by_id_with_role_status(db, id_user)
  if not entity or not entity.user_role:
    return None
  return entity.user_role.name