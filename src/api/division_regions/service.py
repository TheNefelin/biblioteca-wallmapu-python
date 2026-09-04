from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import RegionResponse
from . import repository


async def get_all(db: AsyncSession) -> list[RegionResponse]:
  items = await repository.get_all(db)
  return [RegionResponse.model_validate(item) for item in items]
