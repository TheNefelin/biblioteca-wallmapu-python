from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import CommuneDTO
from . import repository


async def get_all(db: AsyncSession) -> list[CommuneDTO]:
  items = await repository.get_all(db)
  return [CommuneDTO.model_validate(item) for item in items]
