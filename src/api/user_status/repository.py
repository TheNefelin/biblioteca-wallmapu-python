# GET ALL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import dtos, models

# -----------------------------------------------------------------
# GET ALL 
def get_all(db: Session) -> list[dtos.UserStatusDTO]:
  try:
    items = (
      db.query(models.UserStatus)
      .order_by(models.UserStatus.id_user_status.asc())
      .all()
    )
    
    return [dtos.UserStatusDTO.model_validate(item) for item in items]
  except SQLAlchemyError as e:
    raise e
