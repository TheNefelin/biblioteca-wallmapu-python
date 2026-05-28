from sqlalchemy.orm import Session

from . import models

# -----------------------------------------------------------------
# GET ALL 
def get_all(db: Session) -> list[models.UserRole]:
  return (
    db.query(models.UserRole)
    .order_by(models.UserRole.id_user_role.asc())
    .all()
  )
  