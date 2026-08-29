from typing import List
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_202_ACCEPTED

from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.core.database import get_db_async
from src.schemas.dtos import CreateNewsDTO, NewsDTO, NewsWithGalleryDTO, UpdateNewsDTO
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/news", tags=["news"])

# -----------------------------------------------------------------
# GET ALL Pagination
@router.get(
  "/",
  response_model=ApiResponse[PaginationResponseDTO[List[NewsWithGalleryDTO]]],
  status_code=HTTP_200_OK,
  summary="Listar noticias",
  description="Retorna lista paginada de noticias con sus imágenes"
)
async def get_all_pagination(
  request: Request,
  pagination_request: PaginationRequestDTO = Depends(),
  db: AsyncSession = Depends(get_db_async)
):
  try:
    pagination_response = await service.get_all_pagination(db, pagination_request)

    if pagination_response.pages > pagination_response.page:
      params = {"page": pagination_response.page + 1, "limit": pagination_request.limit}
      if pagination_request.search:
        params["search"] = pagination_request.search
      pagination_response.next = str(request.url.include_query_params(**params))

    if pagination_response.page > 1:
      params = {"page": pagination_response.page - 1, "limit": pagination_request.limit}
      if pagination_request.search:
        params["search"] = pagination_request.search
      pagination_response.prev = str(request.url.include_query_params(**params))

    return ApiResponse.success(pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# GET BY ID
@router.get(
  "/{id}",
  response_model=ApiResponse[NewsWithGalleryDTO],
  status_code=HTTP_200_OK,
  summary="Obtener noticia por ID",
  description="Retorna una noticia específica con sus imágenes"
)
async def get_by_id(
  request: Request,
  id: int,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    result = await service.get_by_id(db, id)

    if not result:
      return ApiResponse.not_found()

    return ApiResponse.success(result)
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# CREATE
@router.post(
  "/",
  response_model=ApiResponse[NewsDTO],
  status_code=status.HTTP_201_CREATED,
  summary="Crear noticia",
  description="Crea una nueva noticia (solo admin)",
  dependencies=[admin_required],
)
async def create(
  news: CreateNewsDTO,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    created = await service.create(db, news)

    return ApiResponse.created(created)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# UPDATE
@router.put(
  "/{id}",
  response_model=ApiResponse[NewsDTO],
  status_code=HTTP_202_ACCEPTED,
  summary="Actualizar noticia",
  description="Actualiza una noticia existente (solo admin)",
  dependencies=[admin_required],
)
async def update(
  id: int,
  news: UpdateNewsDTO,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    if (id != news.id_news):
      return ApiResponse.bad_request(message=f"El id: {id} no coincide")

    updated = await service.update(db, id, news)

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
  description="Elimina una noticia (solo admin)",
  dependencies=[admin_required],
)
async def delete(
  id: int,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    await service.delete(db, id)

    return ApiResponse.deleted()
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))