from typing import List, Optional
from unittest import result
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.url_helper import get_base_url
from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from . import dtos, repository

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/books", tags=["books"])

# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/", 
  response_model=ApiResponse[PaginationResponseDTO[List[dtos.BookDTO]]], 
  status_code=HTTP_200_OK
)
def get_all_pagination(
  request: Request,
  page: int = Query(default=1, ge=1, description="Número de página a mostrar"),
  limit: int = Query(default=10, ge=1, le=100, description="Cantidad de elementos por página"),
  search: Optional[str] = Query(default=None, description="Buscar opcional"),
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
# GET ALL BY ID
@router.get(
  "/{id}", 
  response_model=ApiResponse[dtos.BookDTO], 
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
  response_model=ApiResponse[dtos.BookDTO], 
  status_code=HTTP_201_CREATED,
  dependencies=[admin_required]
)
def create_book(
  book: dtos.CreateBookDTO, 
  db: Session = Depends(get_db)
):
  try:
    if book.authors.count == 0:
      return ApiResponse.bad_request(message="El autor es requerido")

    if book.subjects.count == 0:
      return ApiResponse.bad_request(message="El o los descriptores son requerido")

    if book.genre_id == 0:
      return ApiResponse.bad_request(message="El género es requerido")      
    
    result = repository.create(book, db)

    return ApiResponse.success(data=result)
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
      
# -----------------------------------------------------------------
# UPDATE
@router.put(
  "/{id}",
  response_model=ApiResponse[dtos.BookDTO], 
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def update_book(
  id: int, 
  book: dtos.UpdateBookDTO, 
  db: Session = Depends(get_db)
):
  try:
    if book.id_book != id:
      return ApiResponse.bad_request(message="El Id no coincide")

    if book.authors.count == 0:
      return ApiResponse.bad_request(message="El autor es requerido")

    if book.subjects.count == 0:
      return ApiResponse.bad_request(message="El o los descriptores son requerido")

    if book.genre_id == 0:
      return ApiResponse.bad_request(message="El género es requerido")      
      
    result = repository.update(book, db)
    
    if not result:
      return ApiResponse.not_found()

    return ApiResponse.success(data=result)
  except Exception as e:
    return ApiResponse.server_error(message=str(e))

