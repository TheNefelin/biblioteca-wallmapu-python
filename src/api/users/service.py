import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import UUID

from src.schemas.dtos import PaginationRequest, PaginationResponse
from src.schemas.dtos import UserRequest, UserResponse, UserDetailResponse, UserRequest, UserAdminRequest
from src.api.notifications import service as notification_service
from . import repository

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------
# MAPPER: User ORM â†’ UserDetailResponse
def _map_user_to_detail(user) -> UserDetailResponse:
  return UserDetailResponse(
    **UserResponse.model_validate(user).model_dump(),
    commune_name=user.commune.name if user.commune else "",
    user_role_name=user.user_role.name if user.user_role else "",
    user_status_name=user.user_status.name if user.user_status else "",
  )


# -----------------------------------------------------------------
# GET ALL DETAILED (PAGINATED)
async def get_all_detailed(db: AsyncSession, pagination: PaginationRequest) -> PaginationResponse[list[UserDetailResponse]]:
  pagination_response = await repository.get_all_detailed(db, pagination)
  users = pagination_response.data or []

  data = [_map_user_to_detail(user) for user in users]

  return PaginationResponse[list[UserDetailResponse]](
    page=pagination_response.page,
    pages=pagination_response.pages,
    items=pagination_response.items,
    data=data,
  )


# -----------------------------------------------------------------
# GET BY ID DETAILED
async def get_by_id_detailed(db: AsyncSession, id_user: UUID) -> UserDetailResponse | None:
  entity = await repository.get_by_id_detailed(db, id_user)
  if not entity:
    return None
  return _map_user_to_detail(entity)


# -----------------------------------------------------------------
# GET OR CREATE USER (Auth)
async def get_or_create_user(db: AsyncSession, dto: UserRequest) -> UserDetailResponse:
  entity = await repository.get_by_email(db, dto.email)

  if not entity:
    created = await repository.create(db, dto.model_dump(exclude_none=True))

    try:
      await notification_service.create_welcome_notification(
        db=db,
        user_id=str(created.id_user),
        user_email=created.email,
        user_name=created.name,
      )
    except Exception:
      logger.warning(f"Error al enviar notificación de bienvenida para user {created.id_user}")

    return _map_user_to_detail(created)

  return _map_user_to_detail(entity)


# -----------------------------------------------------------------
# UPDATE USER
async def update(db: AsyncSession, id_user: UUID, update_dto: UserRequest) -> UserResponse | None:
  entity = await repository.update(db, id_user, update_dto.model_dump(exclude_unset=True))
  if not entity:
    return None
  return UserResponse.model_validate(entity)


# -----------------------------------------------------------------
# UPDATE USER BY ADMIN
async def update_by_admin(db: AsyncSession, id_user: UUID, update_dto: UserAdminRequest, current_user_id: str) -> UserResponse | None:
  update_data = update_dto.model_dump(exclude_unset=True)

  if str(id_user) == current_user_id:
    update_data.pop("user_role_id", None)
    update_data.pop("user_status_id", None)

  entity = await repository.update(db, id_user, update_data)
  if not entity:
    return None
  return UserResponse.model_validate(entity)


# -----------------------------------------------------------------
# GET ROLE NAME BY USER ID (para security: el rol real se lee de la BD)
async def get_role_name_by_id(db: AsyncSession, id_user: UUID) -> str | None:
  entity = await repository.get_by_id_with_role_status(db, id_user)
  if not entity or not entity.user_role:
    return None
  return entity.user_role.name