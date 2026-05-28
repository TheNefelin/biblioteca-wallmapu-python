from sqlalchemy.orm import Session

from . import models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Region]:
  return (
    db.query(models.Region)
    .order_by(models.Region.region.asc())
    .all()
  )
  