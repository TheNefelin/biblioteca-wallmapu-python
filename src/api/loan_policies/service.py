from sqlalchemy.orm import Session
from . import dtos, repository


# -----------------------------------------------------------------
# GET DEFAULT 
def get_default_policy(db: Session) -> dtos.LoanPolicyDTO | None:
  
  policy = repository.get_default_policy(db)
  if not policy:
    return None

  return dtos.LoanPolicyDTO.model_validate(policy)


# -----------------------------------------------------------------
# UPDATE
def update(db: Session, id: int, data: dtos.LoanPolicyDTO) -> dtos.LoanPolicyDTO | None:
  # Validar que el ID de la ruta coincida con el del DTO
  if data.id_policy and data.id_policy != id:
    raise ValueError(f"ID de ruta ({id}) no coincide con ID del body ({data.id_policy})")
  
  policy = repository.update_policy(db, id, data.model_dump(exclude_unset=True))
  
  if not policy:
    return None
  
  return dtos.LoanPolicyDTO.model_validate(policy)

