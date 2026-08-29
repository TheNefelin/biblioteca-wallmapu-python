from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import RegionDTO
from . import repository


async def get_all(db: AsyncSession) -> list[RegionDTO]:
  items = await repository.get_all(db)
  return [RegionDTO.model_validate(item) for item in items]
