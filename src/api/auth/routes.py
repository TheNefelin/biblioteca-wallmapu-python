from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.core.exceptions import UnauthorizedError
from src.schemas.dtos import AuthGoogleRequest, AuthGoogleResponse
from src.core.database import get_db_async
from src.core.logger import logger
from . import service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/google", response_model=AuthGoogleResponse, status_code=HTTP_200_OK,
  summary="Autenticar con Google",
  description="Valida token de Google, obtiene/crea usuario y devuelve JWT + datos de usuario")
async def auth_google(auth_data: AuthGoogleRequest, db: AsyncSession = Depends(get_db_async)):
  try:
    auth_google_response = await service.auth_service(
      db,
      auth_data.googleToken,
    )

    return auth_google_response
  except ValueError as e:
    logger.error("auth/google error (ValueError): %s", e)
    raise UnauthorizedError(str(e))