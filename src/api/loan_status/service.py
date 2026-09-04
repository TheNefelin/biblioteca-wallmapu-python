from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import LoanStatusResponse
from . import repository


async def get_all(db: AsyncSession) -> list[LoanStatusResponse]:
  items = await repository.get_all(db)
  return [LoanStatusResponse.model_validate(item) for item in items]
