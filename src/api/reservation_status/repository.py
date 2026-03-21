from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import models


# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.ReservationStatus]:
  try:
    return (
      db.query(models.ReservationStatus)
      .order_by(models.ReservationStatus.id_status.asc())
      .all()
    )
  except SQLAlchemyError as e:
    raise e
