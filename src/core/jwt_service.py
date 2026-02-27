from datetime import datetime, timedelta, timezone
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from uuid import UUID
from src.core.config import settings

SECRET_KEY = settings.SECRET_KEY  # Agregar en .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1 #60 * 24 * 7  # (7 días)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def create_access_token(user_id: UUID, role: str) -> str:
  """Crear JWT token para tu backend"""
  now = datetime.now(tz=timezone.utc)
  expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  
  payload = {
    "sub": str(user_id),
    "role": role,    
    "exp": expire,
    "iat": now
  }
  
  return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
  """
  Verifica JWT token y opcionalmente valida rol
  Retorna payload completo si es válido
  """
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return payload
  except JWTError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Token inválido o expirado",
      headers={"WWW-Authenticate": "Bearer"}
    )   

def get_current_user(required_roles: Optional[List[str]] = None):
  """Función que valida token y roles para usar con Depends()"""
  def _get_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    
    # Validar roles si se pasó alguno
    if required_roles is not None:
      role = payload.get("role")
        
      if role not in required_roles:
        raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="No tiene permisos suficientes"
        )
    
    return payload
  return _get_user