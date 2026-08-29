from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.users import service as users_service
from src.core.config import settings
from src.core.database import get_db_async
from src.core.exceptions import ForbiddenError, UnauthorizedError

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 2  # 2h
bearer_scheme = HTTPBearer(auto_error=False)


def create_access_token(user_id: UUID, role: str) -> str:
  """Crea un JWT. El rol embebido es una pista, no la autoridad final."""
  now = datetime.now(tz=timezone.utc)
  payload = {
    "sub": str(user_id),
    "role": role,
    "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    "iat": now,
  }
  return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
  try:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
  except JWTError:
    raise UnauthorizedError()


def get_current_user(required_roles: Optional[list] = None):
  """Valida el JWT y lee el rol REAL del usuario desde la BD en cada request.

  El rol del token es solo una pista; el permiso se consulta en la base para
  que cambios de rol/baja se reflejen al instante (patrón SKILL).
  Acepta lista de roles `UserRole` (str enum), coherente con `src.core.roles`.
  """
  async def _get_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db_async),
  ):
    if credentials is None:
      raise UnauthorizedError()

    payload = verify_token(credentials.credentials)

    try:
      user_id = UUID(str(payload["sub"]))
    except (ValueError, KeyError, TypeError):
      raise UnauthorizedError()

    role = await users_service.get_role_name_by_id(db, user_id)
    if role is None:
      raise UnauthorizedError(message="User no longer exists")

    if required_roles is not None and role not in required_roles:
      raise ForbiddenError()

    payload["role"] = role
    return payload
  return _get_user
