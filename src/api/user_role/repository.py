from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.user_role.dtos import UserRoleDTO
from src.api.user_role.models import UserRole

# GET ALL
def get_all(db: Session):
  try:
    items = db.query(UserRole).order_by(UserRole.id_user_role.asc()).all()
    
    return [UserRoleDTO.model_validate(item) for item in items]
  except SQLAlchemyError as e:
    raise e
  