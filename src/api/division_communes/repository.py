from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Commune]:
  try:
    return (
      db.query(models.Commune)
      .order_by(models.Commune.commune.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e
  