from sqlalchemy.orm import Session
from . import models


def get_all(db: Session) -> list[models.LoanStatus]:
  return (
    db.query(models.LoanStatus)
    .order_by(models.LoanStatus.id_status.asc())
    .all()
  )
