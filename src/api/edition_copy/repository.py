from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from . import dtos, models

# -----------------------------------------------------------------
# GET ALL
def get_all(db: Session) -> list[dtos.EditionCopyDTO]:
  try:
    query = (
      db.query(models.EditionCopy)
      .options(
        joinedload(models.EditionCopy.status)
      )
      .order_by(models.EditionCopy.id_copy.asc())
      .all()
    )
    
    return [dtos.EditionCopyDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# GET BY ID
def get_by_id(id: int, db: Session) -> dtos.EditionCopyDTO:
  try:
    query = (
      db.query(models.EditionCopy)
      .options(
        joinedload(models.EditionCopy.status)
      )
      .filter(models.EditionCopy.id_copy == id)
      .first()
    )
    
    return [dtos.EditionCopyDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e

# -----------------------------------------------------------------
# GET BY EDITION ID
def get_by_edition_id(id: int, db: Session) -> list[dtos.EditionCopyDTO]:
  try:
    query = (
      db.query(models.EditionCopy)
      .options(
        joinedload(models.EditionCopy.status)
      )
      .filter(models.EditionCopy.edition_id == id)
      .order_by(models.EditionCopy.id_copy.asc())
      .all()
    )
    
    return [dtos.EditionCopyDTO.model_validate(item) for item in query]
  except SQLAlchemyError as e:
    raise e


  