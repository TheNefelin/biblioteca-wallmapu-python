from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from src.core.database import get_db_async
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse
from src.schemas.dtos import LoanPolicyDTO
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/loan-policies",
  tags=["loan-policies"],
)


# -----------------------------------------------------------------
# GET DEFAULT
@router.get(
  "/default",
  response_model=ApiResponse[LoanPolicyDTO],
  status_code=HTTP_200_OK,
  summary="Obtener política por defecto",
  description="Retorna la política de préstamo predeterminada"
)
async def get_default_policy(db: AsyncSession = Depends(get_db_async)):
  try:
    res = await service.get_default_policy(db)
    if not res:
      return ApiResponse.not_found(message="No hay política por defecto configurada")
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# UPDATE
@router.put(
  "/{id}",
  response_model=ApiResponse[LoanPolicyDTO],
  status_code=HTTP_200_OK,
  summary="Actualizar política de préstamo",
  description="Actualiza los campos de la política (máximo libros, días, etc.)",
  dependencies=[admin_required]
)
async def update_loan_policy(
  id: int,
  dto: LoanPolicyDTO,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    item = await service.update(db, id, dto)
    return ApiResponse.success(data=item)
  except Exception as e:
    return ApiResponse.server_error(str(e))