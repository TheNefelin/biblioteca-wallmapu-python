from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import CopyStatusDTO
from . import repository


async def get_all(db: AsyncSession) -> list[CopyStatusDTO]:
  items = await repository.get_all(db)
  return [CopyStatusDTO.model_validate(item) for item in items]
