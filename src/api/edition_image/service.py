from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from rfc9457 import BadRequestProblem
from src.api.editions import service as editions_service
from src.core import cloudinary
from src.core.exceptions import NotFoundError

PATH = "edition"


# -----------------------------------------------------------------
# CREATE
async def create_edition_image(file: UploadFile) -> str:
  file_bytes = await file.read()
  url, _ = cloudinary.upload_image_7_10(
    file_bytes=file_bytes,
    folder=f"{PATH}"
  )
  return url


# -----------------------------------------------------------------
# DELETE
async def delete_edition_image(id_edition: int, db: AsyncSession) -> bool:
  edition = await editions_service.get_edition_by_id(db, id_edition)
  if not edition:
    raise NotFoundError(entity="Edición")

  if not edition.cover_image or edition.cover_image.strip() == "":
    raise BadRequestProblem(detail="La edición no tiene imagen")

  public_id = cloudinary.extract_public_id(edition.cover_image)

  if public_id:
    cloudinary.delete_image(public_id)

  await editions_service.update_cover_image(db, id_edition, None)

  return True