from typing import List
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.url_helper import get_base_url
from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/books", tags=["books"])


# -----------------------------------------------------------------
# GET ALL PAGINATION
@router.get(
  "/pagination", 
  response_model=ApiResponse[PaginationResponseDTO[List[dtos.BookDetailDTO]]], 
  status_code=HTTP_200_OK
)
def get_all_pagination(
  request: Request,
  pagination_request: PaginationRequestDTO = Depends(),
  db: Session = Depends(get_db)
):
  pagination_response = service.get_all_pagination(pagination_request, db)
  return ApiResponse.success(pagination_response)


# -----------------------------------------------------------------
# GET ALL BY ID
@router.get(
  "/detail/{id}", 
  response_model=ApiResponse[dtos.BookDetailDTO], 
  status_code=HTTP_200_OK
)
def get_by_id(
  request: Request,
  id: int, 
  db: Session = Depends(get_db)
):
  try:
    result = service.get_book_detail_by_id(id, db)
    
    if not result:
      return ApiResponse.not_found()

    return ApiResponse.success(result)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET BY ID
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
    result = service.get_book_by_id(id, db)
    
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
    if book.genre_id == 0:
      return ApiResponse.bad_request(message="El género es requerido")      
    result = service.create_book(book, db)

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

    if book.genre_id == 0:
      return ApiResponse.bad_request(message="El género es requerido")      

    result = service.update_book(book, db)
    
    if not result:
      return ApiResponse.not_found()

    return ApiResponse.success(data=result)
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def delete_book(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    result = service.delete_book(id, db)

    if result is None:
      return ApiResponse.not_found()

    return ApiResponse.success(data=True)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
