from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED

from src.core.url_helper import get_base_url
from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from src.core import jwt_service, roles, database
from . import repository, dtos

admin_required = Depends(jwt_service.get_current_user(required_roles=[roles.UserRole.ADMIN]))
user_required = Depends(jwt_service.get_current_user(required_roles=[roles.UserRole.LECTOR]))
admin_or_user_required = Depends(jwt_service.get_current_user(required_roles=[roles.UserRole.ADMIN, roles.UserRole.LECTOR]))

router = APIRouter(prefix="/users", tags=["users"])

# -----------------------------------------------------------------
# GET ALL DETAILED
@router.get(
  "/detailed", 
  response_model=ApiResponse[PaginationResponseDTO[List[dtos.UserDetailDTO]]],
  status_code=HTTP_200_OK,
  dependencies=[admin_required],  
)
def get_all_detailed(
  request: Request,
  page: int = Query(default=1, ge=1, description="Número de página a mostrar"),
  limit: int = Query(default=10, ge=1, le=100, description="Cantidad de elementos por página"),
  search: Optional[str] = Query(default=None, description="Buscar en título o subtítulo"),
  db: Session = Depends(database.get_db)
):
  try:
    pagination_request = PaginationRequestDTO(
      page=page,
      limit=limit,
      search=search
    )

    pagination_response = repository.get_all_detailed(pagination_request, db)

    current_page = pagination_response.page
    total_pages = pagination_response.pages

    base_url = get_base_url(request)
    search_param = f"&search={search}" if search else ""

    # NEXT
    if current_page < total_pages:
      pagination_response.next = (
        f"{base_url}?page={current_page + 1}&limit={limit}{search_param}"
      )

    # PREV
    if current_page > 1:
      pagination_response.prev = (
        f"{base_url}?page={current_page - 1}&limit={limit}{search_param}"
      )

    return ApiResponse.success(pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# GET BY ID DETAILED
@router.get(
  "/detailed/{id}", 
  response_model=ApiResponse[dtos.UserDetailDTO],
  status_code=HTTP_200_OK,
  dependencies=[admin_or_user_required],  
)
def get_by_id_detailed(id: UUID, db: Session = Depends(database.get_db)):
  try:  
    res = repository.get_by_id_detailed(id, db)

    if not res:
      return ApiResponse.not_found(message="Usuario no encontrado")

    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# UPDATE USER
@router.put(
  "/{id}", 
  response_model=ApiResponse[dtos.UserDTO],
  status_code=HTTP_201_CREATED,
  dependencies=[user_required],  
)
def update_user(
  id: UUID, update_dto: dtos.UpdateUserDTO, 
  db: Session = Depends(database.get_db),
  current_user = Depends(jwt_service.get_current_user())
):
  try:
    # Solo puede modificar su propio perfil
    if (str(id) != current_user["sub"]):
      return ApiResponse.unauthorized(message='No estas autorizado para modificar este usuario')

    updated_dto = repository.update(id, update_dto, db)
    
    if not updated_dto:
      return ApiResponse.not_found(message="Usuario no encontrado")
    
    return ApiResponse.updated(data=updated_dto)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
  
# -----------------------------------------------------------------
# UPDATE USER BY ADMIN
@router.put(
  "/admin/{id}", 
  response_model=ApiResponse[dtos.UserDTO],
  status_code=HTTP_202_ACCEPTED,
  dependencies=[admin_required],  
)
def update_user(
  id: UUID, update_dto: dtos.UpdateUserByAdminDTO, 
  db: Session = Depends(database.get_db)
):
  try:
    updated_dto = repository.update(id, update_dto, db)
    
    if not updated_dto:
      return ApiResponse.not_found(message="Usuario no encontrado")
    
    return ApiResponse.updated(data=updated_dto)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
  