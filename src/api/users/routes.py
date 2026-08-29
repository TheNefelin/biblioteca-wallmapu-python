from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from starlette.status import HTTP_200_OK

from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.core.database import get_db_async
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))
admin_or_user_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(prefix="/users", tags=["users"])


# -----------------------------------------------------------------
# GET ALL DETAILED (PAGINATED)
@router.get(
  "/pagination",
  response_model=ApiResponse[PaginationResponseDTO[list]],
  status_code=HTTP_200_OK,
  summary="Listar todos los usuarios con paginación",
  description="Retorna lista paginada de usuarios con nombres resueltos (comuna, rol, estado). Incluye búsqueda por nombre, email, rol o estado.",
  dependencies=[admin_required],
)
async def get_all_detailed(
  request: Request,
  pagination_request: PaginationRequestDTO = Depends(),
  db: AsyncSession = Depends(get_db_async)
):
  try:
    pagination_response = await service.get_all_detailed(db, pagination_request)

    if pagination_response.pages > pagination_response.page:
      pagination_response.next = str(request.url.include_query_params(page=pagination_response.page + 1, limit=pagination_request.limit))
    if pagination_response.page > 1:
      pagination_response.prev = str(request.url.include_query_params(page=pagination_response.page - 1, limit=pagination_request.limit))

    return ApiResponse.success(data=pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET BY ID DETAILED
@router.get(
  "/{id}",
  response_model=ApiResponse,
  status_code=HTTP_200_OK,
  summary="Obtener usuario por ID",
  description="Retorna un usuario con todos los datos resueltos (comuna, rol, estado)",
  dependencies=[admin_or_user_required],
)
async def get_by_id_detailed(id: UUID, db: AsyncSession = Depends(get_db_async)):
  try:
    res = await service.get_by_id_detailed(db, id)

    if not res:
      return ApiResponse.not_found(message="Usuario no encontrado")

    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# UPDATE USER (propio perfil)
@router.put(
  "/{id}",
  response_model=ApiResponse,
  status_code=HTTP_200_OK,
  summary="Actualizar perfil propio",
  description="Actualiza los datos de su propio perfil. Solo el usuario autenticado puede modificar su perfil",
)
async def update_user(
  id: UUID, update_dto,
  db: AsyncSession = Depends(get_db_async),
  current_user: dict = Depends(get_current_user(required_roles=[UserRole.LECTOR]))
):
  try:
    if (str(id) != current_user["sub"]):
      return ApiResponse.unauthorized(message='No estas autorizado para modificar este usuario')

    updated_dto = await service.update(db, id, update_dto)

    if not updated_dto:
      return ApiResponse.not_found(message="Usuario no encontrado")

    return ApiResponse.success(data=updated_dto)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# UPDATE USER BY ADMIN
@router.put(
  "/admin/{id}",
  response_model=ApiResponse,
  status_code=HTTP_200_OK,
  summary="Actualizar usuario por administrador",
  description="Actualiza cualquier usuario incluyendo rol y estado. Solo administradores. Si el admin se modifica a sí mismo, no puede cambiar su propio rol ni estado.",
)
async def update_user_by_admin(
  id: UUID, update_dto,
  db: AsyncSession = Depends(get_db_async),
  current_user: dict = Depends(get_current_user(required_roles=[UserRole.ADMIN]))
):
  try:
    updated_dto = await service.update_by_admin(db, id, update_dto, current_user_id=current_user["sub"])

    if not updated_dto:
      return ApiResponse.not_found(message="Usuario no encontrado")

    return ApiResponse.success(data=updated_dto)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))