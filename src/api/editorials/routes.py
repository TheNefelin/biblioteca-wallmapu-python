from typing import List
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db_async
from src.core.exceptions import AppError
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.schemas.dtos import EditorialRequest, EditorialResponse
from src.schemas.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/editorial",
  tags=["editorial"]
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
  response_model=ApiResponse[PaginationResponseDTO[list[EditorialResponse]]],
  status_code=HTTP_200_OK,
  summary="Listar editoriales con paginación",
  description="Obtiene lista paginada de editoriales, opcionalmente filtrada por búsqueda",
  dependencies=[admin_required]
)
async def get_editorial_paginated(
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
  response_model=ApiResponse[List[EditorialResponse]],
  status_code=HTTP_200_OK,
  summary="Listar todas las editoriales",
  description="Obtiene lista completa de editoriales ordenada por nombre",
)
async def get_all_editorial(db: AsyncSession = Depends(get_db_async)):
  try:
    res = await service.get_all(db)
    return ApiResponse.success(data=res)
  except AppError as e:
    return _error_response(e)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET BY ID
@router.get(
  "/{id}",
  response_model=ApiResponse[EditorialResponse],
  status_code=HTTP_200_OK,
  summary="Obtener editorial por ID",
  description="Retorna los datos de una editorial específica",
)
async def get_editorial_by_id(
  id: int,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.get_by_id(db, id)
    if not res:
      return ApiResponse.not_found(message="Editorial no encontrada")
    return ApiResponse.success(data=res)
  except AppError as e:
    return _error_response(e)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# CREATE
@router.post(
  "/",
  response_model=ApiResponse[EditorialResponse],
  status_code=HTTP_201_CREATED,
  summary="Crear una nueva Editorial",
  description="Crea una editorial con el nombre proporcionado",
  dependencies=[admin_required],
)
async def create_editorial(
  dto: EditorialRequest,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.create(db, dto)
    return ApiResponse.created(data=res, message="Editorial creada exitosamente")
  except AppError as e:
    return _error_response(e)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# UPDATE
@router.put(
  "/{id}",
  response_model=ApiResponse[EditorialResponse],
  status_code=HTTP_200_OK,
  summary="Actualizar una Editorial",
  description="Actualiza el nombre de una editorial existente",
  dependencies=[admin_required],
)
async def update_editorial(
  id: int,
  dto: EditorialRequest,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.update(db, id, dto)
    return ApiResponse.success(data=res, message="Editorial modificada exitosamente")
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
  summary="Eliminar una Editorial",
  description="Elimina una editorial por ID",
  dependencies=[admin_required],
)
async def delete_editorial(
  id: int,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.delete(db, id)
    return ApiResponse.success(data=True, message="Editorial eliminada exitosamente")
  except AppError as e:
    return _error_response(e)
  except Exception as e:
    return ApiResponse.server_error(str(e))
