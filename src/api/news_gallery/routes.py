from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.core.security import get_current_user
from src.core.roles import UserRole
from src.core.database import get_db_async
from src.core.exceptions import AppError
from src.schemas.dtos import NewsGalleryDTO
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/news-gallery", tags=["news-gallery"])

# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/news/{news_id}",
  response_model=list[NewsGalleryDTO],
  status_code=HTTP_200_OK,
  summary="Obtener imágenes de una noticia",
  description="Retorna todas las imágenes asociadas a una noticia por su ID"
)
async def get_by_news_id(
  news_id: int,
  db: AsyncSession = Depends(get_db_async)
):
  res = await service.get_by_news_id(db, news_id)

  return res

# -----------------------------------------------------------------
# CREATE
@router.post(
  "/news/{news_id}",
  response_model=list[NewsGalleryDTO],
  status_code=status.HTTP_201_CREATED,
  summary="Subir imágenes a noticia",
  description="Sube hasta 3 imágenes a una noticia existente (solo admin)",
  dependencies=[admin_required],
)
async def create_gallery(
  news_id: int,
  files: list[UploadFile] = File(...),
  alts: list[str] = Form(...),
  db: AsyncSession = Depends(get_db_async)
):
  if len(files) != len(alts):
    raise AppError("La cantidad de imágenes y textos alt no coincide")

  if len(files) > 3:
    raise AppError("Solo se permiten hasta 3 imágenes")

  try:
    result = await service.create_news_gallery_with_images(
      news_id=news_id,
      files=files,
      alts=alts,
      db=db
    )

    return result
  except ValueError as e:
    raise AppError(str(e))

# -----------------------------------------------------------------
# DELETE ALL BY NEWS
@router.delete(
  "/news/{news_id}",
  response_model=object,
  status_code=status.HTTP_202_ACCEPTED,
  summary="Eliminar todas las imágenes de una noticia",
  description="Elimina todas las imágenes asociadas a una noticia (solo admin)",
  dependencies=[admin_required],
)
async def delete_by_news_id(
  news_id: int,
  db: AsyncSession = Depends(get_db_async)
):
  res = await service.delete_news_gallery_by_news_id(db, news_id)

  return res

# -----------------------------------------------------------------
# DELETE BY ID
@router.delete(
  "/{id}",
  response_model=object,
  status_code=status.HTTP_202_ACCEPTED,
  summary="Eliminar una imagen de la galería",
  description="Elimina una imagen específica de la galería por su ID (solo admin)",
  dependencies=[admin_required],
)
async def delete(
  id: int,
  db: AsyncSession = Depends(get_db_async)
):
  res = await service.delete_news_gallery(db, id)

  return res