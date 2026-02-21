from datetime import datetime
import re
from typing import Optional
from pydantic import UUID4, BaseModel, ConfigDict, field_validator

from src.api.communes.dtos import CommuneDTO
from src.api.user_role.dtos import UserRoleDTO
from src.api.user_status.dtos import UserStatusDTO

# USER DTO
class UserDTO(BaseModel): 
  id_user: UUID4
  email: str
  name: Optional[str] = None
  lastname: Optional[str] = None
  rut: Optional[str] = None
  address: Optional[str] = None
  phone: Optional[str] = None
  created_at: datetime
  updated_at: datetime
  commune_id: Optional[int] = None 
  user_role_id: Optional[int] = None 
  user_status_id: Optional[int] = None 

  model_config = ConfigDict(from_attributes=True) # ✅ hace el mapeo

# USER DETAIL DTO
class UserDetailDTO(UserDTO):
  commune: Optional[CommuneDTO] = None
  user_role: UserRoleDTO
  user_status: UserStatusDTO

# UPDATE DTO
class UpdateUserDTO(BaseModel):
  name: Optional[str] = None
  lastname: Optional[str] = None
  rut: Optional[str] = None
  address: Optional[str] = None
  phone: Optional[str] = None
  commune_id: Optional[int] = None  

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
    if not re.match(r'^\d{1,10}$', v):
      raise ValueError('Teléfono debe contener solo números (máximo 10 dígitos)')
    return v

class UpdateUserByAdminDTO(UpdateUserDTO):
  user_role_id: Optional[int] = None 
  user_status_id: Optional[int] = None 
