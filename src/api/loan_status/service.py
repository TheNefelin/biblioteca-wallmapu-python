from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import LoanStatusDTO
from . import repository


async def get_all(db: AsyncSession) -> list[LoanStatusDTO]:
  items = await repository.get_all(db)
  return [LoanStatusDTO.model_validate(item) for item in items]
