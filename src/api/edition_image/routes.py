from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db_async
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.schemas.dtos import ApiResponse
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/edition-image",
  tags=["edition-image"],
  dependencies=[admin_required],
)

# -----------------------------------------------------------------
# CREATE
@router.post(
  "/",
  response_model=ApiResponse[str],
  status_code=status.HTTP_201_CREATED,
  summary="Subir imagen de edición",
  description="Sube una imagen de portada para una edición (solo admin)"
)
async def create_edition_image(
  file: UploadFile = File(...),
):
  try:
    url = await service.create_edition_image(
      file=file,
    )

    return ApiResponse.created(data=url)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))

# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id_edition}",
  response_model=ApiResponse[bool],
  status_code=status.HTTP_200_OK,
  summary="Eliminar imagen de edición",
  description="Elimina la imagen de portada de una edición (solo admin)"
)
async def delete_edition_image(
  id_edition: int,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    result = await service.delete_edition_image(id_edition, db)

    return ApiResponse.success(data=result)
  except Exception as e:
    return ApiResponse.server_error(message=str(e))