# GET ALL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import models

# -----------------------------------------------------------------
# GET ALL 
def get_all(db: Session) -> list[models.UserStatus]:
  try:
    return (
      db.query(models.UserStatus)
      .order_by(models.UserStatus.id_user_status.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e
