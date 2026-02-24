from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import models, dtos

# -----------------------------------------------------------------
# GET ALL 
def get_all(db: Session) -> list[dtos.UserRoleDTO]:
  try:
    items = (
      db.query(models.UserRole)
      .order_by(models.UserRole.id_user_role.asc())
      .all()
    )
    
    return [dtos.UserRoleDTO.model_validate(item) for item in items]
  except SQLAlchemyError as e:
    raise e
  