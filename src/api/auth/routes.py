from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.shared.dtos import ApiResponse
from src.core import database
from . import dtos, service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/google", response_model=ApiResponse[dtos.AuthGoogleResponse], status_code=HTTP_200_OK,
  summary="Autenticar con Google",
  description="Valida token de Google, obtiene/crea usuario y devuelve JWT + datos de usuario")
def auth_google(auth_data: dtos.AuthGoogleRequest, db: Session = Depends(database.get_db)):
  try:
    auth_google_response = service.auth_service(
      db,
      auth_data.googleToken,
    )
 
    return ApiResponse.success(data=auth_google_response)
  except ValueError as e:
    return ApiResponse.unauthorized(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
