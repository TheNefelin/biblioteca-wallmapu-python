from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import LoanPolicyDTO
from . import repository


# -----------------------------------------------------------------
# GET DEFAULT
async def get_default_policy(db: AsyncSession) -> LoanPolicyDTO | None:
  policy = await repository.get_default_policy(db)
  if not policy:
    return None

  return LoanPolicyDTO.model_validate(policy)


# -----------------------------------------------------------------
# UPDATE
async def update(db: AsyncSession, id: int, data: LoanPolicyDTO) -> LoanPolicyDTO | None:
  # Validar que el ID de la ruta coincida con el del DTO
  if data.id_policy and data.id_policy != id:
    raise ValueError(f"ID de ruta ({id}) no coincide con ID del body ({data.id_policy})")

  policy = await repository.update_policy(db, id, data.model_dump(exclude_unset=True))

  if not policy:
    return None

  return LoanPolicyDTO.model_validate(policy)