import cloudinary
import cloudinary.uploader

from src.core.config import settings
from src.core.logger import logger

cloudinary.config(
  cloud_name=settings.CLOUDINARY_CLOUD_NAME,
  api_key=settings.CLOUDINARY_API_KEY,
  api_secret=settings.CLOUDINARY_API_SECRET,
  secure=True
)

# -----------------------------------------------------------------
# UPLOAD 16/9
def upload_image_16_9(
  file_bytes: bytes,
  folder: str,
  public_id: str | None = None
) -> tuple[str, str]:
  """
  Sube una imagen a Cloudinary y la convierte a WebP.
  Retorna la URL pública.
  """
  result = cloudinary.uploader.upload(
    file_bytes,
    folder=folder,
    public_id=public_id,
    format="webp",
    resource_type="image",
    transformation=[
      {
        "width": 1280,
        "height": 720,
        "crop": "fill",
        "gravity": "center",
        "quality": "auto",
      }
    ]
  )
  
  return result["secure_url"], result["public_id"]

# -----------------------------------------------------------------
# UPLOAD 7/10
def upload_image_7_10(
  file_bytes: bytes,
  folder: str,
  public_id: str | None = None
)-> tuple[str, str]:
  """
  Sube una imagen a Cloudinary y la convierte a WebP.
  Retorna la URL pública.
  """
  result = cloudinary.uploader.upload(
    file_bytes,
    folder=folder,
    public_id=public_id,
    format="webp",
    resource_type="image",
    transformation=[
      {
        "width": 700,
        "height": 1000,
        "crop": "fill",
        "gravity": "center",
        "quality": "auto",
      }
    ]
  )
  
  return result["secure_url"], result["public_id"]

# -----------------------------------------------------------------
# DELETE
def delete_image(public_id: str, retries: int = 2) -> bool:
  for attempt in range(retries):
    try:
      result = cloudinary.uploader.destroy(public_id, resource_type="image")
    except Exception as exc:
      if attempt < retries - 1:
        continue
      logger.error("Cloudinary destroy failed for %s: %s", public_id, exc)
      return False
    status = result.get("result") if isinstance(result, dict) else None
    if status in ("ok", "not found"):
      return True
    if attempt < retries - 1:
      continue
    logger.error("Cloudinary destroy returned unexpected status for %s: %s", public_id, result)
    return False
  return False

# -----------------------------------------------------------------
# EXTRACT PUBLIC ID
def extract_public_id(url: str) -> str | None:
  """
  Extrae: myfolder/oslosfszufg1rsfbeqcm
  desde: https://res.cloudinary.com/dsvkbe0mc/image/upload/v1773087504/myfolder/oslosfszufg1rsfbeqcm.webp
  """

  if not url:
    return None

  try:
    after_upload = url.split("/upload/")[1]
    # Saltar el bloque de transformación opcional (c_fill,h_720,q_auto,w_1280,f_webp)
    # hasta la versión (v<timestamp>). Sin esto, destroy() recibe un public_id
    # inválido ("v.../folder/file") y Cloudinary no borra el archivo.
    while after_upload and not after_upload.startswith("v"):
      after_upload = after_upload.split("/", 1)[1]
    parts = after_upload.split("/", 1)[1] if "/" in after_upload else after_upload
    public_id = parts.rsplit(".", 1)[0]

    return public_id
  except Exception:
    return None
