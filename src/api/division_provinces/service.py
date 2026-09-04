from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import ProvinceResponse
from . import repository


async def get_all(db: AsyncSession) -> list[ProvinceResponse]:
  items = await repository.get_all(db)
  return [ProvinceResponse.model_validate(item) for item in items]
