from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional

from src.core.url_helper import get_base_url
from src.shared.dtos import ApiResponse, PaginationResponseDTO
from src.core import jwt_service, roles, database
from . import repository, dtos

admin_required = Depends(jwt_service.get_current_user(required_roles=[roles.UserRole.ADMIN, roles.UserRole.LECTOR]))

#router = APIRouter(prefix="/users", tags=["users"], dependencies=[admin_required])
router = APIRouter(prefix="/users", tags=["users"])

# -----------------------------------------------------------------
# GET ALL DETAILED
@router.get("/detailed", response_model=ApiResponse[PaginationResponseDTO[List[dtos.UserDetailedDTO]]])
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
# GET ALL
@router.get("/", response_model=ApiResponse[List[dtos.UserDTO]])
def get_all_users(db: Session = Depends(database.get_db)):
  try:
    res = repository.get_all(db)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# GET BY ID
@router.get("/{id}", response_model=ApiResponse[dtos.UserDTO])
def get_by_id_user(id: UUID, db: Session = Depends(database.get_db)):
  try:  
    res = repository.get_by_id(id, db)

    if not res:
      return ApiResponse.not_found(message="Usuario no encontrado")

    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# UPDATE
@router.put("/{id}", response_model=ApiResponse[dtos.UserDTO])
def update_user(id: UUID, update_dto: dtos.UpdateUserDTO, db: Session = Depends(database.get_db)):
  try:
    updated_dto = repository.update(id, update_dto, db)
    
    if not updated_dto:
      return ApiResponse.not_found(message="Usuario no encontrado")
    
    return ApiResponse.updated(data=updated_dto)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
  