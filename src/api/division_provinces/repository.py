from sqlalchemy.orm import Session

from . import models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Province]:
  return (
    db.query(models.Province)
    .order_by(models.Province.province.asc())
    .all()
  )
  