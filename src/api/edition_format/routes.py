from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db_async
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.core.exceptions import AppError, NotFoundError
from src.schemas.dtos import EditionFormatResponse
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/edition-format",
  tags=["edition-format"],
  dependencies=[admin_required]
)


# -----------------------------------------------------------------
# UPDATE (reemplaza formatos de la edición; body vacío elimina todos)
@router.put(
  "/{id_edition}",
  response_model=list[EditionFormatResponse],
  status_code=HTTP_201_CREATED,
  summary="Actualizar formatos de una edición",
  description="Reemplaza todos los formatos asociados a una edición. Si el body viene vacío, elimina todos",
)
async def update_edition_format(
  id_edition: int,
  format_ids: list[int] = Body(..., embed=False),
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.update_formats(db, id_edition, format_ids)
    return res
  except ValueError as e:
    raise AppError(str(e))


# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id_edition}/{id_format}",
  response_model=bool,
  status_code=HTTP_200_OK,
  summary="Eliminar formato de una edición",
  description="Elimina una relación específica entre edición y formato",
)
async def delete_edition_format(
  id_edition: int,
  id_format: int,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.delete_format(db, id_edition, id_format)
    if not res:
      raise NotFoundError()
    return res
  except ValueError as e:
    raise AppError(str(e))


# -----------------------------------------------------------------
# DELETE BY ID EDITION
@router.delete(
  "/edition/{id_edition}",
  response_model=bool,
  status_code=HTTP_200_OK,
  summary="Eliminar todos los formatos de una edición",
  description="Elimina todas las relaciones de formato de una edición específica",
)
async def delete_edition_format_by_edition(
  id_edition: int,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.delete_format_by_edition(db, id_edition)
    if not res:
      raise NotFoundError()
    return res
  except ValueError as e:
    raise AppError(str(e))