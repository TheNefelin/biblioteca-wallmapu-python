from typing import Optional
from pydantic import BaseModel, EmailStr
from uuid import UUID

# DTO para request de autenticación
class AuthGoogleRequest(BaseModel):
  googleToken: str

# DTO para el usuario en la respuesta
class AuthUser(BaseModel):
  id_user: UUID  # O str si usas el ID de Google
  email: EmailStr
  name: Optional[str] = None
  picture: Optional[str] = None
  profileComplete: bool
  user_role_id: Optional[int] = None

# DTO para respuesta de autenticación
class AuthGoogleResponse(BaseModel):
  token: str  # JWT de tu backend
  user: AuthUser