import requests

from . import dtos

def verify_google_token(access_token: str) -> dtos.GoogleUserInfo:
  """
  Valida el Access Token de Google y obtiene información del usuario
  """
  try:
    # Llamar a la API de Google para obtener info del usuario
    googleResponse = requests.get(
      'https://www.googleapis.com/oauth2/v2/userinfo',
      headers={'Authorization': f'Bearer {access_token}'}
    )
    
    if googleResponse.status_code != 200:
      raise ValueError(f'Token inválido: {googleResponse.text}')
    
    googleUser = googleResponse.json()
    
    # Extraer información del usuario
    return dtos.GoogleUserInfo(
      google_id=googleUser['id'],
      email=googleUser['email'],
      name=googleUser.get('name'),
      picture=googleUser.get('picture'),
      email_verified=googleUser.get('verified_email', False)
    )
  except requests.RequestException as e:
    raise ValueError(f"Error al validar token de Google: {str(e)}")
  except KeyError as e:
    raise ValueError(f"Respuesta de Google incompleta: {str(e)}")
