from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.api.auth.dtos import GoogleUserInfo
from src.api.users import models, dtos


def get_or_create_user(
  googleUserInfo: GoogleUserInfo,
  db: Session
):
  try:
    user = db.query(models.User).filter(models.User.email == googleUserInfo.email).first()

    if user:
      return user;

    new_user = models.User(
      email=googleUserInfo.email,
      name=googleUserInfo.name,
      user_role_id=3,
      user_status_id=1
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return dtos.UserDTO.model_validate(new_user)
  except IntegrityError as e:
    db.rollback()
    raise ValueError("Error de integridad en la base de datos")  
  except SQLAlchemyError as e:
    db.rollback()
    raise e
