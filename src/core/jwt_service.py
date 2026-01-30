from datetime import datetime, timedelta
from jose import jwt, JWTError
from uuid import UUID
from src.core.config import settings

SECRET_KEY = settings.SECRET_KEY  # Agregar en .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 días

def create_access_token(user_id: UUID) -> str:
  """Crear JWT token para tu backend"""
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  
  payload = {
    "sub": str(user_id),
    "exp": expire,
    "iat": datetime.utcnow()
  }
  
  return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> UUID:
  """Verificar JWT token y retornar user_id"""
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = UUID(payload.get("sub"))
    return user_id
  except JWTError:
    raise ValueError("Token inválido o expirado")