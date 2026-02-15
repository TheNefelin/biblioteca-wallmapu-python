from enum import Enum

class UserRole(str, Enum):
  ADMIN = "Admin"
  LECTOR = "Lector"
