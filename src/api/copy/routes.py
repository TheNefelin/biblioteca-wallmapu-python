from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db_async
from src.core.exceptions import AppError, NotFoundError
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.schemas.dtos import CopyResponse, CopyDetailResponse, CopyRequest
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/copy", tags=["copy"])


# -----------------------------------------------------------------
@router.get(
  "/detail/book/{id_book}",
  response_model=List[CopyDetailResponse],
  status_code=HTTP_200_OK,
  summary="Listar ejemplares con detalle completo por libro",
  description="Retorna todos los ejemplares de un libro con datos de estado, edición, género y autor",
)
async def get_all_copy_detail_by_book(id_book: int, db: AsyncSession = Depends(get_db_async)):
  res = await service.get_all_detail_by_book_id(db, id_book)
  return res


# -----------------------------------------------------------------
@router.get(
  "/edition/{id_edition}",
  response_model=List[CopyResponse],
  status_code=HTTP_200_OK,
  summary="Listar ejemplares por edición (sin anidados)",
  description="Retorna todos los ejemplares de una edición sin datos anidados",
  dependencies=[admin_required],
)
async def get_all_copy_by_edition(id_edition: int, db: AsyncSession = Depends(get_db_async)):
  res = await service.get_all_by_edition_id(db, id_edition)
  return res


# -----------------------------------------------------------------
@router.post(
  "/",
  response_model=CopyResponse,
  status_code=HTTP_201_CREATED,
  summary="Crear nuevo ejemplar",
  description="Crea un nuevo ejemplar asociado a una edición",
  dependencies=[admin_required],
)
async def create_copy(copy: CopyRequest, db: AsyncSession = Depends(get_db_async)):
  try:
    res = await service.create(db, copy)
    return res
  except ValueError as e:
    raise AppError(str(e))


# -----------------------------------------------------------------
@router.put(
  "/{id}",
  response_model=CopyResponse,
  status_code=HTTP_200_OK,
  summary="Actualizar ejemplar",
  description="Actualiza un ejemplar existente por ID",
  dependencies=[admin_required],
)
async def update_copy(id: int, copy: CopyRequest, db: AsyncSession = Depends(get_db_async)):
  try:
    res = await service.update(db, id, copy)
    if not res:
      raise NotFoundError("Ejemplar")
    return res
  except ValueError as e:
    raise AppError(str(e))


# -----------------------------------------------------------------
@router.delete(
  "/{id}",
  response_model=bool,
  status_code=HTTP_200_OK,
  summary="Eliminar ejemplar",
  description="Elimina un ejemplar por ID",
  dependencies=[admin_required],
)
async def delete_copy(id: int, db: AsyncSession = Depends(get_db_async)):
  try:
    res = await service.delete(db, id)
    if not res:
      raise NotFoundError("Ejemplar")
    return res
  except ValueError as e:
    raise AppError(str(e))