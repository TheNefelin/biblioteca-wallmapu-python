from sqlalchemy.ext.asyncio import AsyncSession

from rfc9457 import BadRequestProblem
from src.schemas.dtos import AuthUserResponse, AuthGoogleResponse, AuthGoogleRequest, UserRequest
from src.api.users import service as user_service
from src.core import security
from . import google_service


async def auth_service(
  db: AsyncSession,
  google_token: str,
):
  # 1. valida token y devuelve usuario de google, o arroja error
  google_user_info = await google_service.verify_google_token(google_token)

  # 2. Valida que el correo este verificado en Google
  if not google_user_info.email_verified:
    raise BadRequestProblem(detail=f"Email no verificado en Google")

  # 3. obtener o crear usuario
  user = UserRequest(
    email=google_user_info.email,
    name=google_user_info.name,
  )

  user = await user_service.get_or_create_user(db, user)

  if not user.user_role_name:
    raise BadRequestProblem(detail="El usuario no tiene un rol asignado")

  # 4. generar JWT de tu backend
  token = security.create_access_token(
    user.id_user,
    user.user_role_name
  )

  # 5. verificar si el perfil estÃ¡ completo
  profile_complete = bool(
    user.name and
    user.lastname and
    user.rut
  )

  # 6. prepara usuario
  auth_user = AuthUserResponse(
    id_user=user.id_user,
    email=user.email,
    name=user.name,
    picture=google_user_info.picture,
    profileComplete=profile_complete,
    role=user.user_role_name
  )

  # 7. devuelve token y usuario autenticado
  auth_google_response = AuthGoogleResponse(
    token=token,
    user=auth_user
  )

  return auth_google_response