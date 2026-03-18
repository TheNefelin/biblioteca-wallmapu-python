from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Region]:
  try:
    return (
      db.query(models.Region)
      .order_by(models.Region.region.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e
  