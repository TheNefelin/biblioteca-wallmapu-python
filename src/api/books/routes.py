from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/books", tags=["books"])


# -----------------------------------------------------------------
@router.get(
  "/pagination", 
  response_model=ApiResponse[PaginationResponseDTO[List[dtos.BookDetailDTO]]], 
  status_code=HTTP_200_OK,
  summary="Listar libros con paginación (DTO plano)",
  description="Retorna lista paginada con DTO plano (autor, género, portada, conteos)",
  dependencies=[admin_required],
)
def get_all_pagination(
  request: Request,
  pagination_request: PaginationRequestDTO = Depends(),
  db: Session = Depends(get_db)
):
  try:
    pagination_response = service.get_all_pagination(db, pagination_request)

    if pagination_response.pages > pagination_response.page:
      pagination_response.next = str(request.url.include_query_params(page=pagination_response.page + 1, limit=pagination_request.limit))
    if pagination_response.page > 1:
      pagination_response.prev = str(request.url.include_query_params(page=pagination_response.page - 1, limit=pagination_request.limit))

    return ApiResponse.success(pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
@router.get(
  "/{id}", 
  response_model=ApiResponse[dtos.BookDTO], 
  status_code=HTTP_200_OK,
  summary="Obtener libro por ID",
  description="Retorna un libro con género, autores y descriptores",
  dependencies=[admin_required],
)
def get_book_by_id(
  id: int, 
  db: Session = Depends(get_db)
):
  try:
    result = service.get_book_by_id(db, id)
    
    if not result:
      return ApiResponse.not_found()

    return ApiResponse.success(result)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
@router.post(
  "/",
  response_model=ApiResponse[dtos.BookDTO], 
  status_code=HTTP_201_CREATED,
  summary="Crear nuevo libro",
  description="Crea un libro con autores y descriptores asociados",
  dependencies=[admin_required],
)
def create_book(
  book: dtos.CreateBookDTO, 
  db: Session = Depends(get_db)
):
  try:
    result = service.create_book(db, book)
    return ApiResponse.success(data=result)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
@router.put(
  "/{id}",
  response_model=ApiResponse[dtos.BookDTO], 
  status_code=HTTP_200_OK,
  summary="Actualizar libro",
  description="Actualiza un libro existente con autores y descriptores",
  dependencies=[admin_required],
)
def update_book(
  id: int, 
  book: dtos.UpdateBookDTO, 
  db: Session = Depends(get_db)
):
  if book.id_book != id:
    return ApiResponse.bad_request(message="El Id no coincide")

  try:
    result = service.update_book(db, book)
    
    if not result:
      return ApiResponse.not_found()

    return ApiResponse.success(data=result)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
@router.delete(
  "/{id}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  summary="Eliminar libro",
  description="Elimina un libro si no tiene dependencias (autores, descriptores, ediciones, reservas, préstamos activos)",
  dependencies=[admin_required],
)
def delete_book(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    result = service.delete_book(db, id)

    if not result:
      return ApiResponse.not_found()

    return ApiResponse.success(data=True)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
