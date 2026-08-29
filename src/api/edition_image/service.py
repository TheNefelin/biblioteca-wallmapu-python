from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.editions import repository as edition_repository
from src.core import cloudinary

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
  item = await edition_repository.get_entity_by_id(db, id_edition)
  if not item:
    raise ValueError("La ediciÃ³n no existe")

  if not item.cover_image or item.cover_image.strip() == "":
    raise ValueError("La ediciÃ³n no tiene imagen")

  public_id = cloudinary.extract_public_id(item.cover_image)

  if public_id:
    cloudinary.delete_image(public_id)

  item.cover_image = None
  await db.commit()

  return True