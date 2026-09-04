from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import UserStatusResponse
from . import repository


async def get_all(db: AsyncSession) -> list[UserStatusResponse]:
  items = await repository.get_all(db)
  return [UserStatusResponse.model_validate(item) for item in items]
