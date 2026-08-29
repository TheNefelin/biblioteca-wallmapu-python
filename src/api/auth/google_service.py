import httpx

from src.schemas.dtos import GoogleUserInfo


async def verify_google_token(access_token: str) -> GoogleUserInfo:
  """
  Valida el Access Token de Google y obtiene información del usuario
  """
  try:
    async with httpx.AsyncClient(timeout=10) as client:
      googleResponse = await client.get(
        'https://www.googleapis.com/oauth2/v2/userinfo',
        headers={'Authorization': f'Bearer {access_token}'},
      )
  except httpx.HTTPError as e:
    raise ValueError(f"Error al validar token de Google: {str(e)}")

  if googleResponse.status_code != 200:
    raise ValueError(f'Token inválido: {googleResponse.text}')

  googleUser = googleResponse.json()

  try:
    # Extraer información del usuario
    return GoogleUserInfo(
      google_id=googleUser['id'],
      email=googleUser['email'],
      name=googleUser.get('name'),
      picture=googleUser.get('picture'),
      email_verified=googleUser.get('verified_email', False)
    )
  except KeyError as e:
    raise ValueError(f"Respuesta de Google incompleta: {str(e)}")