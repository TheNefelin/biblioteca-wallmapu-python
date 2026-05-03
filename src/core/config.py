from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  DATABASE_URL: str
  SECRET_KEY: str
  GOOGLE_CLIENT_ID: str
  DEBUG: bool = False

  CLOUDINARY_CLOUD_NAME: str
  CLOUDINARY_API_KEY: str
  CLOUDINARY_API_SECRET: str

  BREVO_API_KEY: Optional[str] = None
  BREVO_FROM_EMAIL: Optional[str] = None

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore" # ✅ Ignorar variables extra del .env
  )

settings = Settings()