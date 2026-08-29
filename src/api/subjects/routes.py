from typing import List
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db_async
from src.core.exceptions import AppError
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.schemas.dtos import SubjectRequest, SubjectResponse
from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/subject",
  tags=["subject"],
)


def _error_response(e: AppError) -> ApiResponse:
  return ApiResponse(
    isSuccess=False,
    statusCode=e.status_code,
    message=e.message,
    data=None,
  )


# -----------------------------------------------------------------
# GET ALL PAGINATION
@router.get(
  "/pagination",
  response_model=ApiResponse[PaginationResponseDTO[list[SubjectResponse]]],
  status_code=HTTP_200_OK,
  summary="Listar descriptores con paginación",
  description="Obtiene lista paginada de descriptores, opcionalmente filtrada por búsqueda",
  dependencies=[admin_required]
)
async def get_subjects_paginated(
  request: Request,
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  db: AsyncSession = Depends(get_db_async),
):
  try:
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

    return ApiResponse.success(data=pagination_response)
  except AppError as e:
    return _error_response(e)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/",
  response_model=ApiResponse[List[SubjectResponse]],
  status_code=HTTP_200_OK,
  summary="Listar todos los descriptores",
  description="Obtiene lista completa de descriptores ordenada por nombre",
)
async def get_all_subject(db: AsyncSession = Depends(get_db_async)):
  try:
    res = await service.get_all(db)
    return ApiResponse.success(data=res)
  except AppError as e:
    return _error_response(e)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# CREATE
@router.post(
  "/",
  response_model=ApiResponse[SubjectResponse],
  status_code=HTTP_201_CREATED,
  summary="Crear un nuevo Descriptor",
  description="Crea un descriptor con el nombre proporcionado",
  dependencies=[admin_required],
)
async def create_subject(
  dto: SubjectRequest,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.create(db, dto)
    return ApiResponse.created(data=res, message="Descriptor creado exitosamente")
  except AppError as e:
    return _error_response(e)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# UPDATE
@router.put(
  "/{id}",
  response_model=ApiResponse[SubjectResponse],
  status_code=HTTP_200_OK,
  summary="Actualizar un Descriptor",
  description="Actualiza el nombre de un descriptor existente",
  dependencies=[admin_required],
)
async def update_subject(
  id: int,
  dto: SubjectRequest,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.update(db, id, dto)
    return ApiResponse.success(data=res, message="Descriptor modificado exitosamente")
  except AppError as e:
    return _error_response(e)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  summary="Eliminar un Descriptor",
  description="Elimina un descriptor. Falla si está asociado a libros",
  dependencies=[admin_required],
)
async def delete_subject(
  id: int,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.delete(db, id)
    return ApiResponse.success(data=True, message="Descriptor eliminado exitosamente")
  except AppError as e:
    return _error_response(e)
  except Exception as e:
    return ApiResponse.server_error(str(e))
