from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from starlette.status import HTTP_200_OK

from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from src.core import jwt_service, roles, database
from . import dtos, service

admin_required = Depends(jwt_service.get_current_user(required_roles=[roles.UserRole.ADMIN]))
user_required = Depends(jwt_service.get_current_user(required_roles=[roles.UserRole.LECTOR]))
admin_or_user_required = Depends(jwt_service.get_current_user(required_roles=[roles.UserRole.ADMIN, roles.UserRole.LECTOR]))

router = APIRouter(prefix="/users", tags=["users"])


# -----------------------------------------------------------------
# GET ALL DETAILED (PAGINATED)
@router.get(
  "/pagination",
  response_model=ApiResponse[PaginationResponseDTO[list[dtos.UserDetailDTO]]],
  status_code=HTTP_200_OK,
  summary="Listar todos los usuarios con paginación",
  description="Retorna lista paginada de usuarios con nombres resueltos (comuna, rol, estado). Incluye búsqueda por nombre, email, rol o estado.",
  dependencies=[admin_required],
)
def get_all_detailed(
  pagination_request: PaginationRequestDTO = Depends(),
  db: Session = Depends(database.get_db)
):
  try:
    pagination_response = service.get_all_detailed(db, pagination_request)
    return ApiResponse.success(data=pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET BY ID DETAILED
@router.get(
  "/{id}",
  response_model=ApiResponse[dtos.UserDetailDTO],
  status_code=HTTP_200_OK,
  summary="Obtener usuario por ID",
  description="Retorna un usuario con todos los datos resueltos (comuna, rol, estado)",
  dependencies=[admin_or_user_required],
)
def get_by_id_detailed(id: UUID, db: Session = Depends(database.get_db)):
  try:
    res = service.get_by_id_detailed(db, id)

    if not res:
      return ApiResponse.not_found(message="Usuario no encontrado")

    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# UPDATE USER (propio perfil)
@router.put(
  "/{id}",
  response_model=ApiResponse[dtos.UserDTO],
  status_code=HTTP_200_OK,
  summary="Actualizar perfil propio",
  description="Actualiza los datos de su propio perfil. Solo el usuario autenticado puede modificar su perfil",
  dependencies=[user_required],
)
def update_user(
  id: UUID, update_dto: dtos.UpdateUserDTO,
  db: Session = Depends(database.get_db),
  current_user = Depends(jwt_service.get_current_user())
):
  try:
    if (str(id) != current_user["sub"]):
      return ApiResponse.unauthorized(message='No estas autorizado para modificar este usuario')

    updated_dto = service.update(db, id, update_dto)

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
  response_model=ApiResponse[dtos.UserDTO],
  status_code=HTTP_200_OK,
  summary="Actualizar usuario por administrador",
  description="Actualiza cualquier usuario incluyendo rol y estado. Solo administradores",
  dependencies=[admin_required],
)
def update_user_by_admin(
  id: UUID, update_dto: dtos.UpdateUserByAdminDTO,
  db: Session = Depends(database.get_db)
):
  try:
    updated_dto = service.update(db, id, update_dto)

    if not updated_dto:
      return ApiResponse.not_found(message="Usuario no encontrado")

    return ApiResponse.success(data=updated_dto)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
  