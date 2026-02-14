# GET ALL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.user_status.dtos import UserStatusDTO
from src.api.user_status.models import UserStatus


def get_all(db: Session):
  try:
    items = db.query(UserStatus).order_by(UserStatus.id_user_status.asc()).all()
    
    return [UserStatusDTO.model_validate(item) for item in items]
  except SQLAlchemyError as e:
    raise e