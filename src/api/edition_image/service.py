from fastapi import UploadFile
from sqlalchemy.orm import Session

from src.api.editions import repository as edition_repository
from src.services import cloudinary_service

PATH = "edition"


# -----------------------------------------------------------------
# CREATE
def create_edition_image(file: UploadFile) -> str:
  url, _ = cloudinary_service.upload_image_7_10(
    file_bytes=file.file.read(),
    folder=f"{PATH}"
  )
  return url


# -----------------------------------------------------------------
# DELETE
def delete_edition_image(id_edition: int, db: Session) -> bool:
  item = edition_repository.get_entity_by_id(db, id_edition)
  if not item:
    raise ValueError("La edición no existe")

  if not item.cover_image or item.cover_image.strip() == "":
    raise ValueError("La edición no tiene imagen")

  public_id = cloudinary_service.extract_public_id(item.cover_image)

  if public_id:
    cloudinary_service.delete_image(public_id)

  item.cover_image = None
  db.commit()

  return True
