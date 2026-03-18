from fastapi import Query
from sqlalchemy.orm import Session
from . import models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[models.Author]:
  return (
    db.query(models.Author)
    .order_by(models.Author.name.asc())
    .all()
  )
