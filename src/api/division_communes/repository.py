from sqlalchemy.orm import Session

from . import models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Commune]:
  return (
    db.query(models.Commune)
    .order_by(models.Commune.name.asc())
    .all()
  )
  