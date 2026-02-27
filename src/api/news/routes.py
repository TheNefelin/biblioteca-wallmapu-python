
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_202_ACCEPTED

from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
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
  limit: int = Query(default=10, ge=1, le=100, description="Cantidad de elementos por página"),
  search: Optional[str] = Query(default=None, description="Buscar en título o subtítulo"),
  db: Session = Depends(get_db)
):
  try:
    pagination_request = PaginationRequestDTO(
      page=page,
      limit=limit,
      search=search
    )
    
    pagination_response = repository.get_all_pagination(pagination_request, db)

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
