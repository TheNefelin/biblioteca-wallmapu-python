from fastapi import UploadFile
from sqlalchemy.orm import Session

from src.api.editions import repository as edition_repository
from src.services.cloudinary_service import delete_image, upload_image_7_10

PATH = "edition"

# -----------------------------------------------------------------
# CREATE
def create_edition_image(
  file: UploadFile,
) -> str:
  public_id = None

  try:
    url, public_id = upload_image_7_10(
      file_bytes=file.file.read(),
      folder=f"{PATH}"
    )

    return url    
  except Exception as e:
    try:
      delete_image(public_id)
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
    item = edition_repository.get_by_id(id_edition, db) 

    if not item:
      raise ValueError("La edición no existe")

    if not item.cover_image or item.cover_image.strip() == "":
      raise ValueError("La edición no tiene imagen")

    public_id = extract_public_id(item.cover_image)

    if public_id:
      delete_image(public_id)

    item.cover_image = None
    db.commit()      

    return True
  except Exception as e:
    raise e

def extract_public_id(url: str) -> str | None:
  """
  Extrae: edition/oslosfszufg1rsfbeqcm
  desde: https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773087504/edition/oslosfszufg1rsfbeqcm.webp
  """

  if not url:
    return None
  
  try:
    after_upload = url.split("/upload/")[1]   # Quitar todo antes de /upload/
    parts = after_upload.split("/", 1)[1]     # Quitar la versión (v1770756121)
    public_id = parts.rsplit(".", 1)[0]       # Quitar extensión

    return public_id
  except Exception:
    return None
