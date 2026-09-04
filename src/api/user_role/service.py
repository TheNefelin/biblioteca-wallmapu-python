from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.dtos import UserRoleResponse
from . import repository


async def get_all(db: AsyncSession) -> list[UserRoleResponse]:
  items = await repository.get_all(db)
  return [UserRoleResponse.model_validate(item) for item in items]
