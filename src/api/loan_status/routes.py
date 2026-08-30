from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.core.database import get_db_async
from src.schemas.dtos import LoanStatusDTO
from src.schemas.dtos import ApiResponse
from . import service

router = APIRouter(
  prefix="/loan-status",
  tags=["loan-status"],
)

@router.get(
  "/",
  response_model=ApiResponse[List[LoanStatusDTO]],
  status_code=HTTP_200_OK,
  summary="Listar estados de préstamo",
  description="Obtiene lista completa de estados de préstamo ordenada por ID",
)
async def get_all_loan_status(db: AsyncSession = Depends(get_db_async)):
  try:
    res = await service.get_all(db)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))
