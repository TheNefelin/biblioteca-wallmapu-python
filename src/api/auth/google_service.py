import requests
from typing import Optional
from pydantic import BaseModel

class GoogleUserInfo(BaseModel):
  google_id: str
  email: str
  name: Optional[str] = None
  picture: Optional[str] = None
  email_verified: bool

def verify_google_token(access_token: str) -> GoogleUserInfo:
  """
  Valida el Access Token de Google y obtiene información del usuario
  """
  try:
    # Llamar a la API de Google para obtener info del usuario
    response = requests.get(
      'https://www.googleapis.com/oauth2/v2/userinfo',
      headers={'Authorization': f'Bearer {access_token}'}
    )
    
    if response.status_code != 200:
      raise ValueError(f'Token inválido: {response.text}')
    
    data = response.json()
    
    # Extraer información del usuario
    return GoogleUserInfo(
      google_id=data['id'],
      email=data['email'],
      name=data.get('name'),
      picture=data.get('picture'),
      email_verified=data.get('verified_email', False)
    )
    
  except requests.RequestException as e:
    raise ValueError(f"Error al validar token de Google: {str(e)}")
  except KeyError as e:
    raise ValueError(f"Respuesta de Google incompleta: {str(e)}")