from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import CopyStatusResponse
from . import repository


async def get_all(db: AsyncSession) -> list[CopyStatusResponse]:
  items = await repository.get_all(db)
  return [CopyStatusResponse.model_validate(item) for item in items]
