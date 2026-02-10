import cloudinary
import cloudinary.uploader

from src.core.config import settings

cloudinary.config(
  cloud_name=settings.CLOUDINARY_CLOUD_NAME,
  api_key=settings.CLOUDINARY_API_KEY,
  api_secret=settings.CLOUDINARY_API_SECRET,
  secure=True
)

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
        "fetch_format": "auto"
      }
    ]
  )
  
  return result["secure_url"], result["public_id"]

def delete_image(public_id: str):
  cloudinary.uploader.destroy(
    public_id,
    resource_type="image"
  )