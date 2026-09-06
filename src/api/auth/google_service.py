import httpx

from src.core.config import settings
from src.schemas.dtos import GoogleUserInfoResponse

GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


async def _fetch_userinfo(client: httpx.AsyncClient, access_token: str) -> dict:
  response = await client.get(
    GOOGLE_USERINFO_URL,
    headers={"Authorization": f"Bearer {access_token}"},
  )
  return response.json() if response.status_code == 200 else {}


async def verify_google_token(access_token: str) -> GoogleUserInfoResponse:
  """
  Valida el Access Token de Google y obtiene información del usuario.

  Verifica que el token fue emitido para ESTA aplicación (aud == GOOGLE_CLIENT_ID).
  Sin este check, cualquier access token de Google válido (emitido a otra app)
  permitiría autenticarse en el backend.
  """
  try:
    async with httpx.AsyncClient(timeout=10) as client:
      response = await client.get(
        GOOGLE_TOKEN_INFO_URL,
        params={"access_token": access_token},
      )
  except httpx.HTTPError as e:
    raise ValueError(f"Error al validar token de Google: {str(e)}")

  if response.status_code != 200:
    raise ValueError(f"Token inválido: {response.text}")

  token_info = response.json()

  # Validar que el token fue emitido para esta aplicación
  if settings.GOOGLE_CLIENT_ID and token_info.get("aud") != settings.GOOGLE_CLIENT_ID:
    raise ValueError("Token inválido: no fue emitido para esta aplicación")

  email_verified = token_info.get("email_verified")
  if email_verified not in (True, "true"):
    raise ValueError("Email no verificado en Google")

  # /tokeninfo no garantiza name/picture con un access token; si faltan, se
  # consultan de /userinfo (misma validez: el token ya fue validado por aud).
  userinfo = {}
  if not token_info.get("picture") or not token_info.get("name"):
    try:
      async with httpx.AsyncClient(timeout=10) as client:
        userinfo = await _fetch_userinfo(client, access_token)
    except httpx.HTTPError:
      userinfo = {}

  try:
    return GoogleUserInfoResponse(
      google_id=token_info["sub"],
      email=token_info["email"],
      name=userinfo.get("name") or token_info.get("name"),
      picture=userinfo.get("picture") or token_info.get("picture"),
      email_verified=True,
    )
  except KeyError as e:
    raise ValueError(f"Respuesta de Google incompleta: {str(e)}")