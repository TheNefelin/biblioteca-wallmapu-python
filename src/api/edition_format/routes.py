from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse
from . import dtos, service

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
  response_model=ApiResponse[list[dtos.EditionFormatDTO]],
  status_code=HTTP_201_CREATED,
  summary="Actualizar formatos de una edición",
  description="Reemplaza todos los formatos asociados a una edición. Si el body viene vacío, elimina todos",
)
def update_edition_format(
  id_edition: int,
  format_ids: list[int] = Body(..., embed=False),
  db: Session = Depends(get_db)
):
  try:
    res = service.update_formats(db, id_edition, format_ids)
    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id_edition}/{id_format}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  summary="Eliminar formato de una edición",
  description="Elimina una relación específica entre edición y formato",
)
def delete_edition_format(
  id_edition: int,
  id_format: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.delete_format(db, id_edition, id_format)
    if not res:
      return ApiResponse.not_found()
    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# DELETE BY ID EDITION
@router.delete(
  "/edition/{id_edition}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  summary="Eliminar todos los formatos de una edición",
  description="Elimina todas las relaciones de formato de una edición específica",
)
def delete_edition_format_by_edition(
  id_edition: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.delete_format_by_edition(db, id_edition)
    if not res:
      return ApiResponse.not_found()
    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
