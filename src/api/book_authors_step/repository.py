from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from . import dtos, models

# -----------------------------------------------------------------  
# DELETE
def delete(item: dtos.BookAuthorDTO, db: Session) -> bool:
  try:
    relation = db.get(
      models.BookAuthor,
      (item.id_book, item.id_author)
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