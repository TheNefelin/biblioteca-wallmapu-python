from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import UserStatusDTO
from . import repository


async def get_all(db: AsyncSession) -> list[UserStatusDTO]:
  items = await repository.get_all(db)
  return [UserStatusDTO.model_validate(item) for item in items]
