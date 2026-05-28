from datetime import datetime
import re
from typing import Optional
from pydantic import UUID4, BaseModel, ConfigDict, Field, field_validator


class CreateUser(BaseModel):
  """DTO para crear un nuevo usuario (usado por Auth)"""
  email: str = Field(..., description="Correo electrónico del usuario")
  name: str = Field(..., description="Nombre del usuario")


class UpdateUserDTO(BaseModel):
  """DTO para actualizar perfil de usuario (campos opcionales)"""
  name: Optional[str] = Field(None, description="Nombre del usuario")
  lastname: Optional[str] = Field(None, description="Apellido del usuario")
  rut: Optional[str] = Field(None, description="RUT del usuario (formato 12345678-9)")
  address: Optional[str] = Field(None, description="Dirección del usuario")
  phone: Optional[str] = Field(None, description="Teléfono del usuario (máximo 10 dígitos)")
  commune_id: Optional[int] = Field(None, description="ID de la comuna")

  @field_validator('rut')
  @classmethod
  def validate_rut(cls, v):
    if v is None:
      return v
    if not re.match(r'^\d{7,8}-[\dkK]$', v):
      raise ValueError('RUT debe tener formato 12345678-9')
    return v
  
  @field_validator('phone')
  @classmethod
  def validate_phone(cls, v):
    if v is None:
      return v
    if not re.match(r'^\d{1,9}$', v):
      raise ValueError('Teléfono debe contener solo números (máximo 9 dígitos)')
    return v


class UpdateUserByAdminDTO(UpdateUserDTO):
  """DTO para actualizar usuario por administrador (incluye rol y estado)"""
  user_role_id: Optional[int] = Field(None, description="ID del rol del usuario")
  user_status_id: Optional[int] = Field(None, description="ID del estado del usuario")


class UserDTO(BaseModel):
  """DTO base de usuario con todos los campos del modelo"""
  id_user: UUID4 = Field(..., description="UUID único del usuario")
  email: str = Field(..., description="Correo electrónico del usuario")
  name: Optional[str] = Field(None, description="Nombre del usuario")
  lastname: Optional[str] = Field(None, description="Apellido del usuario")
  rut: Optional[str] = Field(None, description="RUT del usuario")
  address: Optional[str] = Field(None, description="Dirección del usuario")
  phone: Optional[str] = Field(None, description="Teléfono del usuario")
  created_at: datetime = Field(..., description="Fecha de creación del registro")
  updated_at: datetime = Field(..., description="Fecha de última actualización")
  commune_id: Optional[int] = Field(None, description="ID de la comuna")
  user_role_id: Optional[int] = Field(None, description="ID del rol del usuario")
  user_status_id: Optional[int] = Field(None, description="ID del estado del usuario")

  model_config = ConfigDict(from_attributes=True)


class UserDetailDTO(UserDTO):
  """DTO plano para listados con nombres resueltos de relaciones"""
  commune_name: Optional[str] = Field(None, description="Nombre de la comuna")
  user_role_name: Optional[str] = Field(None, description="Nombre del rol del usuario")
  user_status_name: Optional[str] = Field(None, description="Nombre del estado del usuario")

