from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import ProvinceDTO
from . import repository


async def get_all(db: AsyncSession) -> list[ProvinceDTO]:
  items = await repository.get_all(db)
  return [ProvinceDTO.model_validate(item) for item in items]
