from sqlalchemy.orm import Session
from . import models


# -----------------------------------------------------------------
# GET DEFAULT 
def get_default_policy(db: Session) -> models.LoanPolicy | None:
  return db.query(models.LoanPolicy).first()


# -----------------------------------------------------------------
# UPDATE
def update_policy(db: Session, id: int, data: dict) -> models.LoanPolicy | None:
  policy = (
    db.query(models.LoanPolicy)
    .filter(models.LoanPolicy.id_policy == id)
    .first()
  )
  
  if not policy:
    return None
  
  for key, value in data.items():
    setattr(policy, key, value)
  
  db.commit()
  db.refresh(policy)
  
  return policy
