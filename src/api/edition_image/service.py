from re import A
from fastapi import UploadFile
from sqlalchemy.orm import Session

from src.api.editions import repository as edition_repository
from src.services import cloudinary_service

PATH = "edition"

# -----------------------------------------------------------------
# CREATE
def create_edition_image(
  file: UploadFile,
) -> str:
  public_id = None

  try:
    url, public_id = cloudinary_service.upload_image_7_10(
      file_bytes=file.file.read(),
      folder=f"{PATH}"
    )

    return url    
  except Exception as e:
    try:
      cloudinary_service.delete_image(public_id)
    except Exception:
      pass  # opcional: loggear error

    raise e

# -----------------------------------------------------------------
# DELETE
def delete_edition_image(
  id_edition: int,
  db: Session
) -> bool:
  try:
    item = edition_repository.get_entity_by_id(id_edition, db) 
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
  except Exception as e:
    raise e


