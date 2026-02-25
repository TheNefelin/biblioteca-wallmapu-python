from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.SubjectDTO]:
  try:
    query = db.query(models.Subject).all()    
    return [dtos.SubjectDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e