from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Editorial]:
  try:
    return (
      db.query(models.Editorial)
      .order_by(models.Editorial.name.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e
