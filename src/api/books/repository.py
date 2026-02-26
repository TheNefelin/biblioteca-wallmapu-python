from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.BookDTO]:
  try:
    query = (
      db.query(models.Book)
      .order_by(models.Book.title.asc())
      .all()  
    )

    return [dtos.BookDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e
