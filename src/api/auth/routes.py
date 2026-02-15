from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.shared.dtos import ApiResponse
from src.core import jwt_service, database
from . import dtos, repository, google_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/google", response_model=ApiResponse[dtos.AuthGoogleResponse], status_code=HTTP_200_OK)
def auth_google(auth_data: dtos.AuthGoogleRequest, db: Session = Depends(database.get_db)):
  try:
    # 1. Validar Access Token con Google
    google_user_info = google_service.verify_google_token(auth_data.googleToken)
    
    if not google_user_info.email_verified:
      return ApiResponse.bad_request(message="Email no verificado en Google")
    
    # 2. Obtener o crear usuario (sin picture)
    user = repository.get_or_create_user(google_user_info, db)
    
    # 3. Generar JWT de tu backend
    token = jwt_service.create_access_token(user.id_user)
    
    # 4. Verificar si el perfil está completo
    profile_complete = bool(
      user.name and 
      user.lastname and 
      user.rut
    )

    auth_user = dtos.AuthUser (
      id_user = user.id_user,
      email = user.email,
      name = user.name,
      picture = google_user_info.picture,
      profileComplete = profile_complete,
      role=user.user_role.role
    )
    
    auth_google_response = dtos.AuthGoogleResponse(
      token=token,
      user=auth_user
    )

    return ApiResponse.success(data=auth_google_response)
  except ValueError as e:
    return ApiResponse.unauthorized(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
