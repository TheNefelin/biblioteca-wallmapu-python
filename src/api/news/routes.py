
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_202_ACCEPTED, HTTP_204_NO_CONTENT

from src.shared.dtos import ApiResponse, PaginationResponseDTO
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.core.url_helper import get_base_url
from src.core.database import get_db
from . import repository, dtos

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/news", tags=["news"])

# -----------------------------------------------------------------
# GET ALL Pagination
@router.get(
  "/", 
  response_model=ApiResponse[PaginationResponseDTO[List[dtos.NewsWithGalleryDTO]]], 
  status_code=HTTP_200_OK
)
def get_all_pagination(
  request: Request,
  page: int = Query(default=1, ge=1, description="Número de página a mostrar"),
  items: int = Query(default=10, ge=1, le=100, description="Cantidad de elementos por página"),
  search: Optional[str] = Query(default=None, description="Buscar en título o subtítulo"),
  db: Session = Depends(get_db)
):
  try:
    count, pages, result = repository.get_all_pagination(page, items, search, db)
    
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

    return ApiResponse.success(paginationResult)
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# GET BY ID Pagination    
@router.get(
  "/{id}", 
  response_model=ApiResponse[dtos.NewsWithGalleryDTO], 
  status_code=HTTP_200_OK
)
def get_by_id(
  request: Request,
  id: int, 
  db: Session = Depends(get_db)
):
  try:
    result = repository.get_by_id(id, db)

    if not result:
      return ApiResponse.not_found()

    return ApiResponse.success(result)  
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# CREATE
@router.post(
  "/", 
  response_model=ApiResponse[dtos.NewsDTO], 
  status_code=status.HTTP_201_CREATED
)
def create(
  news: dtos.CreateNewsDTO, 
  db: Session = Depends(get_db), 
  current_user: dict = admin_required
):
  try:
    created = repository.create(news, db)

    return ApiResponse.created(created)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# UPDATE
@router.put(
  "/{id}", 
  response_model=ApiResponse[dtos.NewsDTO], 
  status_code=HTTP_202_ACCEPTED
)
def update(
  id: int, 
  news: dtos.UpdateNewsDTO, 
  db: Session = Depends(get_db), 
  current_user: dict = admin_required
):
  try:
    if (id != news.id_news):
      return ApiResponse.bad_request(message=f"El id: {id} no coincide")

    updated = repository.update(id, news, db)
    
    if not updated:
      return ApiResponse.not_found(message=f"El id: {id} no se encontró")
    
    return ApiResponse.updated(updated)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id}", 
  response_model=ApiResponse[object], 
  status_code=HTTP_202_ACCEPTED
)
def delete(
  id: int, 
  db: Session = Depends(get_db), 
  current_user: dict = admin_required
):
  try:
    deleted = repository.delete(id, db)

    return ApiResponse.deleted()
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))   
