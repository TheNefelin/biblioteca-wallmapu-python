from pydantic import BaseModel, ConfigDict
from datetime import datetime

# -----------------------------------------------------------------
class UserRoleDTO(BaseModel):
  id_user_role: int
  name: str
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)
  