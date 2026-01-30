from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.api.users import models
from typing import Optional

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
  """Obtener usuario por email"""
  return db.query(models.User).filter(models.User.email == email).first()

def create_user_from_google(
  db: Session, 
  email: str, 
  name: Optional[str], 
  google_id: str  # ✅ Ya no recibe picture
) -> models.User:
  """Crear usuario desde datos de Google"""
  try:
    new_user = models.User(
      email=email,
      name=name,
      # No guardamos picture
      user_role_id=3,
      user_status_id=1
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
  except IntegrityError as e:
    db.rollback()
    raise ValueError("Error al crear usuario desde Google")

def get_or_create_user_from_google(
  db: Session,
  email: str,
  name: Optional[str],
  google_id: str  # ✅ Ya no recibe picture
) -> tuple[models.User, bool]:
  """
  Obtener usuario existente o crear uno nuevo
  Returns: (user, is_new)
  """
  user = get_user_by_email(db, email)
  
  if user:
    return (user, False)
  
  # Usuario nuevo
  new_user = create_user_from_google(db, email, name, google_id)
  return (new_user, True)