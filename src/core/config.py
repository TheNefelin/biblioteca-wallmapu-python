from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  DATABASE_URL: str
  SECRET_KEY: str
  GOOGLE_CLIENT_ID: str
  DEBUG: bool = False

  CLOUDINARY_CLOUD_NAME: str
  CLOUDINARY_API_KEY: str
  CLOUDINARY_API_SECRET: str

  RESEND_API_KEY: str
  RESEND_FROM_EMAIL: str

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore"  # ✅ Ignorar variables extra del .env
  )

settings = Settings()