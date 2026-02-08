from PIL import Image
import os
from io import BytesIO

BASE_DIR = os.getcwd()
STATIC_NEWS_PATH = os.path.join(BASE_DIR, "static", "news")

os.makedirs(STATIC_NEWS_PATH, exist_ok=True)

def save_image_webp(file_bytes: bytes, filename: str) -> str:
  """
  Convierte la imagen a webp y la guarda en static/news
  Retorna el nombre del archivo guardado
  """
  # Abrir imagen desde bytes
  img = Image.open(BytesIO(file_bytes)).convert("RGB")

  # Generar ruta final
  base_name = os.path.splitext(filename)[0]
  webp_filename = f"{base_name}.webp"
  save_path = os.path.join(STATIC_NEWS_PATH, webp_filename)

  # Guardar en webp
  img.save(save_path, "WEBP")

  return webp_filename
