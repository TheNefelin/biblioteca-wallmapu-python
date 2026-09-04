from typing import List
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db_async
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.core.exceptions import NotFoundError, AppError
from src.schemas.dtos import PaginationRequest, PaginationResponse
from src.schemas.dtos import BookResponse, BookDetailResponse, BookRequest
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/books", tags=["books"])


# -----------------------------------------------------------------
@router.get(
  "/pagination",
  response_model=PaginationResponse[List[BookDetailResponse]],
  status_code=HTTP_200_OK,
  summary="Listar libros con paginación (DTO plano)",
  description="Retorna lista paginada con DTO plano (autor, género, portada, conteos)",
  dependencies=[admin_required],
)
async def get_all_pagination(
  request: Request,
  pagination_request: PaginationRequest = Depends(),
  db: AsyncSession = Depends(get_db_async)
):
  pagination_response = await service.get_all_pagination(db, pagination_request)

  if pagination_response.pages > pagination_response.page:
    pagination_response.next = str(request.url.include_query_params(page=pagination_response.page + 1, limit=pagination_request.limit))
  if pagination_response.page > 1:
    pagination_response.prev = str(request.url.include_query_params(page=pagination_response.page - 1, limit=pagination_request.limit))

  return pagination_response


# -----------------------------------------------------------------
@router.get(
  "/{id}",
  response_model=BookResponse,
  status_code=HTTP_200_OK,
  summary="Obtener libro por ID",
  description="Retorna un libro con género, autores y descriptores",
)
async def get_book_by_id(
  id: int,
  db: AsyncSession = Depends(get_db_async)
):
  result = await service.get_book_by_id(db, id)

  if not result:
    raise NotFoundError()

  return result


# -----------------------------------------------------------------
@router.post(
  "/",
  response_model=BookResponse,
  status_code=HTTP_201_CREATED,
  summary="Crear nuevo libro",
  description="Crea un libro con autores y descriptores asociados",
  dependencies=[admin_required],
)
async def create_book(
  book: BookRequest,
  db: AsyncSession = Depends(get_db_async)
):
  result = await service.create_book(db, book)
  return result


# -----------------------------------------------------------------
@router.put(
  "/{id}",
  response_model=BookResponse,
  status_code=HTTP_200_OK,
  summary="Actualizar libro",
  description="Actualiza un libro existente con autores y descriptores",
  dependencies=[admin_required],
)
async def update_book(
  id: int,
  book: BookRequest,
  db: AsyncSession = Depends(get_db_async)
):
  result = await service.update_book(db, id, book)

  if not result:
    raise NotFoundError()

  return result


# -----------------------------------------------------------------
@router.delete(
  "/{id}",
  response_model=bool,
  status_code=HTTP_200_OK,
  summary="Eliminar libro",
  description="Elimina un libro si no tiene dependencias (autores, descriptores, ediciones, reservas, préstamos activos)",
  dependencies=[admin_required],
)
async def delete_book(
  id: int,
  db: AsyncSession = Depends(get_db_async)
):
  result = await service.delete_book(db, id)

  if not result:
    raise NotFoundError()

  return True