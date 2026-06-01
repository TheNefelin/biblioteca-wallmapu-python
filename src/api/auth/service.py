from sqlalchemy.orm import Session

from src.api.users import service as user_service, dtos as user_dto
from src.core import jwt_service
from . import dtos, google_service

def auth_service(
  db: Session,
  google_token: str,
):
  # 1. valida token y devuelve usaurio de google, o arroja error
  google_user_info = google_service.verify_google_token(google_token)

  # 2. Valida que el correo este verificado en Google
  if not google_user_info.email_verified:
    raise ValueError(f"Email no verificado en Google")

  # 3. obtener o crear usuario
  user = user_dto.CreateUser(
    email=google_user_info.email,
    name=google_user_info.name,
  )
  
  user = user_service.get_or_create_user(db, user)

  if not user.user_role_name:
    raise ValueError("El usuario no tiene un rol asignado")

  # 4. generar JWT de tu backend
  token = jwt_service.create_access_token(
    user.id_user, 
    user.user_role_name
  )
  
  # 5. verificar si el perfil está completo
  profile_complete = bool(
    user.name and 
    user.lastname and 
    user.rut
  )

  # 6. prepara usuario
  auth_user = dtos.AuthUser (
    id_user = user.id_user,
    email = user.email,
    name = user.name,
    picture = google_user_info.picture,
    profileComplete = profile_complete,
    role=user.user_role_name
  )    

  # 7. devuelve token y usuario auenticado
  auth_google_response = dtos.AuthGoogleResponse(
    token=token,
    user=auth_user
  )

  return auth_google_response