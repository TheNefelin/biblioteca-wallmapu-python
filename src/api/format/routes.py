from typing import List
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db_async
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.schemas.dtos import FormatRequest, FormatResponse
from src.schemas.dtos import PaginationRequestDTO, PaginationResponseDTO
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/format",
  tags=["format"]
)


# -----------------------------------------------------------------
# GET ALL PAGINATION
@router.get(
  "/pagination",
  response_model=PaginationResponseDTO[list[FormatResponse]],
  status_code=HTTP_200_OK,
  summary="Listar formatos con paginación",
  description="Obtiene lista paginada de formatos, opcionalmente filtrada por búsqueda",
  dependencies=[admin_required]
)
async def get_format_paginated(
  request: Request,
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  db: AsyncSession = Depends(get_db_async),
):
  pagination_request = PaginationRequestDTO[None](
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
  response_model=List[FormatResponse],
  status_code=HTTP_200_OK,
  summary="Listar todos los formatos",
  description="Obtiene lista completa de formatos ordenada por nombre",
)
async def get_all_format(db: AsyncSession = Depends(get_db_async)):
  return await service.get_all(db)


# -----------------------------------------------------------------
# CREATE
@router.post(
  "/",
  response_model=FormatResponse,
  status_code=HTTP_201_CREATED,
  summary="Crear un nuevo Formato",
  description="Crea un formato con el nombre proporcionado",
  dependencies=[admin_required],
)
async def create_format(
  dto: FormatRequest,
  db: AsyncSession = Depends(get_db_async)
):
  return await service.create(db, dto)


# -----------------------------------------------------------------
# UPDATE
@router.put(
  "/{id}",
  response_model=FormatResponse,
  status_code=HTTP_200_OK,
  summary="Actualizar un Formato",
  description="Actualiza el nombre de un formato existente",
  dependencies=[admin_required],
)
async def update_format(
  id: int,
  dto: FormatRequest,
  db: AsyncSession = Depends(get_db_async)
):
  return await service.update(db, id, dto)


# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id}",
  response_model=bool,
  status_code=HTTP_200_OK,
  summary="Eliminar un Formato",
  description="Elimina un formato. Falla si está asociado a ediciones",
  dependencies=[admin_required],
)
async def delete_format(
  id: int,
  db: AsyncSession = Depends(get_db_async)
):
  return await service.delete(db, id)
