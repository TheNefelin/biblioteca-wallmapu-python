from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Province]:
  try:
    return (
      db.query(models.Province)
      .order_by(models.Province.province.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e
  