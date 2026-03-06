from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from . import dtos, models

# -----------------------------------------------------------------  
# DELETE
def delete(item: dtos.BookSubjectDTO, db: Session) -> bool:
  try:
    relation = db.get(
      models.BookSubject,
      (item.id_book, item.id_subject)
    )

    print(item)    
    print(relation)

    if not relation:
      return False

    db.delete(relation)
    db.commit()

    return True
  except IntegrityError as e:
    db.rollback()
    raise ValueError("Error de integridad en la base de datos")  
  except SQLAlchemyError as e:
    db.rollback()
    raise e  
