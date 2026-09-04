from typing import List
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db_async
from src.core.exceptions import AppError
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.schemas.dtos import GenreRequest, GenreResponse
from src.schemas.dtos import PaginationRequest, PaginationResponse
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/genre",
  tags=["genre"]
)


# -----------------------------------------------------------------
# GET ALL PAGINATION
@router.get(
  "/pagination",
  response_model=PaginationResponse[list[GenreResponse]],
  status_code=HTTP_200_OK,
  summary="Listar géneros con paginación",
  description="Obtiene lista paginada de géneros, opcionalmente filtrada por búsqueda",
  dependencies=[admin_required]
)
async def get_genre_paginated(
  request: Request,
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  db: AsyncSession = Depends(get_db_async),
):
  pagination_request = PaginationRequest[None](
    page=page,
    limit=limit,
    search=search or "",
    filter=None,
  )

  pagination_response = await service.get_all_pagination(db, pagination_request)

  if pagination_response.pages > pagination_response.page:
    pagination_response.next = str(request.url.include_query_params(page=pagination_response.page + 1, limit=pagination_request.limit))
  if pagination_response.page > 1:
    pagination_response.prev = str(request.url.include_query_params(page=pagination_response.page - 1, limit=pagination_request.limit))

  return pagination_response


# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/",
  response_model=List[GenreResponse],
  status_code=HTTP_200_OK,
  summary="Listar todos los géneros",
  description="Obtiene lista completa de géneros ordenada por nombre",
)
async def get_all_genre(db: AsyncSession = Depends(get_db_async)):
  res = await service.get_all(db)
  return res


# -----------------------------------------------------------------
# CREATE
@router.post(
  "/",
  response_model=GenreResponse,
  status_code=HTTP_201_CREATED,
  summary="Crear un nuevo Género",
  description="Crea un género con el nombre proporcionado",
  dependencies=[admin_required],
)
async def create_genre(
  dto: GenreRequest,
  db: AsyncSession = Depends(get_db_async)
):
  res = await service.create(db, dto)
  return res


# -----------------------------------------------------------------
# UPDATE
@router.put(
  "/{id}",
  response_model=GenreResponse,
  status_code=HTTP_200_OK,
  summary="Actualizar un Género",
  description="Actualiza el nombre de un género existente",
  dependencies=[admin_required],
)
async def update_genre(
  id: int,
  dto: GenreRequest,
  db: AsyncSession = Depends(get_db_async)
):
  res = await service.update(db, id, dto)
  return res


# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id}",
  response_model=bool,
  status_code=HTTP_200_OK,
  summary="Eliminar un Género",
  description="Elimina un género. Falla si está asociado a libros",
  dependencies=[admin_required],
)
async def delete_genre(
  id: int,
  db: AsyncSession = Depends(get_db_async)
):
  res = await service.delete(db, id)
  return res
