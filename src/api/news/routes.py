
from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_202_ACCEPTED

from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.core.url_helper import get_base_url
from src.core.database import get_db
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/news", tags=["news"])

# -----------------------------------------------------------------
# GET ALL Pagination
@router.get(
  "/", 
  response_model=ApiResponse[PaginationResponseDTO[List[dtos.NewsWithGalleryDTO]]], 
  status_code=HTTP_200_OK,
  summary="Listar noticias",
  description="Retorna lista paginada de noticias con sus imágenes"
)
def get_all_pagination(
  request: Request,
  pagination_request: PaginationRequestDTO = Depends(),
  db: Session = Depends(get_db)
):
  try:
    pagination_response = service.get_all_pagination(db, pagination_request)

    current_page = pagination_response.page
    total_pages = pagination_response.pages

    base_url = get_base_url(request)
    search_param = f"&search={pagination_request.search}" if pagination_request.search else ""

    # NEXT
    if current_page < total_pages:
      pagination_response.next = (
        f"{base_url}?page={current_page + 1}&limit={pagination_request.limit}{search_param}"
      )

    # PREV
    if current_page > 1:
      pagination_response.prev = (
        f"{base_url}?page={current_page - 1}&limit={pagination_request.limit}{search_param}"
      )

    return ApiResponse.success(pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# GET BY ID    
@router.get(
  "/{id}", 
  response_model=ApiResponse[dtos.NewsWithGalleryDTO], 
  status_code=HTTP_200_OK,
  summary="Obtener noticia por ID",
  description="Retorna una noticia específica con sus imágenes"
)
def get_by_id(
  request: Request,
  id: int, 
  db: Session = Depends(get_db)
):
  try:
    result = service.get_by_id(db, id)

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
  status_code=status.HTTP_201_CREATED,
  summary="Crear noticia",
  description="Crea una nueva noticia (solo admin)"
)
def create(
  news: dtos.CreateNewsDTO, 
  db: Session = Depends(get_db), 
  current_user: dict = admin_required
):
  try:
    created = service.create(db, news)

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
  status_code=HTTP_202_ACCEPTED,
  summary="Actualizar noticia",
  description="Actualiza una noticia existente (solo admin)"
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

    updated = service.update(db, id, news)
    
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
  status_code=HTTP_202_ACCEPTED,
  summary="Eliminar noticia",
  description="Elimina una noticia (solo admin)"
)
def delete(
  id: int, 
  db: Session = Depends(get_db), 
  current_user: dict = admin_required
):
  try:
    service.delete(db, id)

    return ApiResponse.deleted()
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))   
