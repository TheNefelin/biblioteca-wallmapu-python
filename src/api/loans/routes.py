from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db_async
from src.core.security import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from src.schemas.dtos import CreateLoanDTO, LoanDTO, LoanDetailDTO, LoanFilterDTO
from . import service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))
user_required = Depends(get_current_user(required_roles=[UserRole.LECTOR]))

router = APIRouter(
  prefix="/loans",
  tags=["loans"],
)


# -----------------------------------------------------------------
# GET ALL PAGINATION
@router.get(
  "/pagination",
  response_model=ApiResponse[PaginationResponseDTO[list[LoanDetailDTO]]],
  status_code=HTTP_200_OK,
  summary="Listar todos los préstamos con paginación",
  description="Retorna lista paginada de préstamos. Filtros: id_status (1=activo, 2=devuelto, 3=vencido)",
  dependencies=[admin_required]
)
async def get_loans_paginated(
  request: Request,
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  id_status: int = Query(default=0),
  db: AsyncSession = Depends(get_db_async)
):
  try:
    filter = LoanFilterDTO(id_status=id_status) if id_status > 0 else None

    pagination_request = PaginationRequestDTO[LoanFilterDTO](
      page=page,
      limit=limit,
      search=search or "",
      filter=filter
    )

    pagination_response = await service.get_all_pagination(db, pagination_request)

    if pagination_response.pages > pagination_response.page:
      pagination_response.next = str(request.url.include_query_params(page=pagination_response.page + 1, limit=limit))
    if pagination_response.page > 1:
      pagination_response.prev = str(request.url.include_query_params(page=pagination_response.page - 1, limit=limit))

    return ApiResponse.success(data=pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET USER RESERVATIONS PAGINATION (Usuario actual)
@router.get(
  "/pagination/user",
  response_model=ApiResponse[PaginationResponseDTO[list[LoanDetailDTO]]],
  status_code=HTTP_200_OK,
  summary="Listar todos los préstamos con paginación",
  description="Retorna lista paginada de préstamos por usuario. Filtros: id_status (1=activo, 2=devuelto, 3=vencido)",
  dependencies=[user_required]
)
async def get_loans_paginated_by_user(
  request: Request,
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  id_status: int = Query(default=0),
  current_user: dict = Depends(get_current_user()),
  db: AsyncSession = Depends(get_db_async)
):
  try:
    user_id = UUID(current_user["sub"])

    filter = LoanFilterDTO(id_status=id_status) if id_status > 0 else None

    pagination_request = PaginationRequestDTO[LoanFilterDTO](
      page=page,
      limit=limit,
      search=search or "",
      filter=filter
    )

    pagination_response = await service.get_all_pagination_by_user(db, user_id, pagination_request)

    if pagination_response.pages > pagination_response.page:
      pagination_response.next = str(request.url.include_query_params(page=pagination_response.page + 1, limit=limit))
    if pagination_response.page > 1:
      pagination_response.prev = str(request.url.include_query_params(page=pagination_response.page - 1, limit=limit))

    return ApiResponse.success(data=pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET ALL OVERDUE
@router.get(
  "/overdue",
  response_model=ApiResponse[List[LoanDetailDTO]],
  status_code=HTTP_200_OK,
  summary="Listar préstamos vencidos",
  description="Retorna todos los préstamos cuya fecha de vencimiento pasó y aún no han sido devueltos",
  dependencies=[admin_required]
)
async def get_overdue_loans(db: AsyncSession = Depends(get_db_async)):
  try:
    res = await service.get_overdue(db)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET ACTIVE LOAN BY BARCODE
@router.get(
  "/copy/{barcode}",
  response_model=ApiResponse[LoanDetailDTO],
  status_code=HTTP_200_OK,
  summary="Buscar préstamo activo por barcode",
  description="Busca un préstamo activo escaneando el barcode del ejemplar",
  dependencies=[admin_required]
)
async def get_active_loan_by_barcode(
  barcode: str,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.get_active_by_barcode(db, barcode)
    if not res:
      return ApiResponse.not_found(message="No hay préstamo activo con este barcode")
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# CREATE
@router.post(
  "/",
  response_model=ApiResponse[LoanDTO],
  status_code=HTTP_201_CREATED,
  summary="Crear un nuevo préstamo",
  description="Crea un nuevo préstamo. La fecha de vencimiento se calcula automáticamente según las políticas de préstamo",
  dependencies=[admin_required]
)
async def create_loan(
  dto: CreateLoanDTO,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.create(db, dto)
    return ApiResponse.created(data=res, message="Préstamo creado exitosamente")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# UPDATE - RETURN BY COPY ID
@router.put(
  "/copy/{id}/return",
  response_model=ApiResponse[LoanDTO],
  status_code=HTTP_200_OK,
  summary="Registrar devolución por código de exemplar",
  description="Registra la devolución de un préstamo escaneando el código del ejemplar",
  dependencies=[admin_required]
)
async def return_loan_by_copy(
  id: int,
  db: AsyncSession = Depends(get_db_async)
):
  try:
    res = await service.return_loan_by_copy_id(db, id)
    if not res:
      return ApiResponse.not_found(message="No hay préstamo activo para este ejemplar")
    return ApiResponse.success(data=res, message="Devolución registrada")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# UPDATE - EXPIRE OVERDUE
@router.put(
  "/expire-overdue",
  response_model=ApiResponse[int],
  status_code=HTTP_200_OK,
  summary="Marcar como vencidos los préstamos vencidos",
  description="Actualiza el estado de préstamos vencidos (fecha de vencimiento pasada y no devueltos) a estado vencido",
  dependencies=[admin_required]
)
async def expire_overdue_loans(db: AsyncSession = Depends(get_db_async)):
  try:
    count = await service.expire_overdue_loans(db)
    return ApiResponse.success(data=count, message=f"{count} préstamos marcados como vencidos")
  except Exception as e:
    return ApiResponse.server_error(str(e))