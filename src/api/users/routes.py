from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED

from src.core.url_helper import get_base_url
from src.shared.dtos import ApiResponse, PaginationResponseDTO
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
  dependencies=[admin_required],
  status_code=HTTP_200_OK
)
def get_all_detailed(
  request: Request,
  page: int = Query(default=1, ge=1, description="Número de página a mostrar"),
  items: int = Query(default=10, ge=1, le=100, description="Cantidad de elementos por página"),
  search: Optional[str] = Query(default=None, description="Buscar en título o subtítulo"),
  db: Session = Depends(database.get_db)
):
  try:
    count, pages, result = repository.get_all_detailed(page, items, search, db)

    # Ajuste automático de página
    if page > pages and pages > 0:
      page = pages
      count, pages, result = repository.get_all_pagination(page, items, search, db)

    # Construir URLs next/prev
    search_param = f"&search={search}" if search else ""
    
    next_url = None
    prev_url = None
    
    base_url = get_base_url(request)
  
    if page < pages:
      next_url = f"{base_url}?page={page + 1}&page_size={items}{search_param}"
    
    if page > 1:
      prev_url = f"{base_url}?page={page - 1}&page_size={items}{search_param}"

    paginationResult = PaginationResponseDTO(  
      items=count,
      pages=pages,
      next=next_url,
      prev=prev_url,
      result=result
    )
    
    return ApiResponse.success(data=paginationResult)
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# GET BY ID DETAILED
@router.get(
  "/detailed/{id}", 
  response_model=ApiResponse[dtos.UserDetailDTO],
  dependencies=[admin_or_user_required],
  status_code=HTTP_200_OK
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
  dependencies=[user_required],
  status_code=HTTP_201_CREATED
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
  dependencies=[admin_required],
  status_code=HTTP_202_ACCEPTED
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
  