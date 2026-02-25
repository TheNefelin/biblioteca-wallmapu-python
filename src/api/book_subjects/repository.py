from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.SubjectDTO]:
  try:
    query = (
      db.query(models.Subject)
      .order_by(models.Subject.subject.asc())
      .all()
    )

    return [dtos.SubjectDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e