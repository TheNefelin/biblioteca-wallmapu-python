from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse, PaginationRequestDTO, PaginationResponseDTO
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))
user_required = Depends(get_current_user(required_roles=[UserRole.LECTOR]))
user_or_admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(
  prefix="/loans",
  tags=["loans"],
)


# -----------------------------------------------------------------
# GET ALL PAGINATION
@router.get(
  "/pagination",
  response_model=ApiResponse[PaginationResponseDTO[list[dtos.LoanDetailDTO]]],
  status_code=HTTP_200_OK,
  summary="Listar todos los préstamos con paginación",
  description="Retorna lista paginada de préstamos. Filtros: id_status (1=activo, 2=devuelto, 3=vencido)",
  dependencies=[admin_required]
)
def get_loans_paginated(
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  id_status: int = Query(default=0),
  db: Session = Depends(get_db)
):
  try:
    filter = dtos.LoanFilterDTO(id_status=id_status) if id_status > 0 else None
    
    pagination_request = PaginationRequestDTO[dtos.LoanFilterDTO](
      page=page,
      limit=limit,
      search=search or "",
      filter=filter
    )

    pagination_response = service.get_all_pagination(db, pagination_request)
    return ApiResponse.success(data=pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET USER RESERVATIONS PAGINATION (Usuario actual)
@router.get(
  "/pagination/user",
  response_model=ApiResponse[PaginationResponseDTO[list[dtos.LoanDetailDTO]]],
  status_code=HTTP_200_OK,
  summary="Listar todos los préstamos con paginación",
  description="Retorna lista paginada de préstamos por usuario. Filtros: id_status (1=activo, 2=devuelto, 3=vencido)",
  dependencies=[user_required]
)
def get_loans_paginated_by_user(
  page: int = Query(default=1, ge=1),
  limit: int = Query(default=10, ge=1, le=100),
  search: str = Query(default=""),
  id_status: int = Query(default=0),
  current_user = Depends(get_current_user()),
  db: Session = Depends(get_db)
):
  try:
    user_id = UUID(current_user["sub"])

    filter = dtos.LoanFilterDTO(id_status=id_status) if id_status > 0 else None
    
    pagination_request = PaginationRequestDTO[dtos.LoanFilterDTO](
      page=page,
      limit=limit,
      search=search or "",
      filter=filter
    )

    pagination_response = service.get_all_pagination_by_user(db, user_id, pagination_request)
    return ApiResponse.success(data=pagination_response)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET ALL OVERDUE
@router.get(
  "/overdue",
  response_model=ApiResponse[List[dtos.LoanDTO]],
  status_code=HTTP_200_OK,
  summary="Listar préstamos vencidos",
  description="Retorna todos los préstamos cuya fecha de vencimiento pasó y aún no han sido devueltos",
  dependencies=[admin_required]
)
def get_overdue_loans(db: Session = Depends(get_db)):
  try:
    res = service.get_overdue(db)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# GET BY ID
@router.get(
  "/{id}",
  response_model=ApiResponse[dtos.LoanDTO],
  status_code=HTTP_200_OK,
  summary="Obtener un préstamo por ID",
  dependencies=[user_or_admin_required]
)
def get_loan_by_id(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_by_id(db, id)
    if not res:
      return ApiResponse.not_found(message="Préstamo no encontrado")
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# CREATE
@router.post(
  "/",
  response_model=ApiResponse[dtos.LoanDTO],
  status_code=HTTP_201_CREATED,
  summary="Crear un nuevo préstamo",
  description="Crea un nuevo préstamo. La fecha de vencimiento se calcula automáticamente según las políticas de préstamo",
  dependencies=[admin_required]
)
def create_loan(
  dto: dtos.CreateLoanDTO,
  db: Session = Depends(get_db)
):
  try:
    res = service.create(db, dto)
    return ApiResponse.created(data=res, message="Préstamo creado exitosamente")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))


# -----------------------------------------------------------------
# UPDATE - RETURN BY COPY ID
@router.put(
  "/copy/{id}/return",
  response_model=ApiResponse[dtos.LoanDTO],
  status_code=HTTP_200_OK,
  summary="Registrar devolución por código de exemplar",
  description="Registra la devolución de un préstamo escaneando el código del exemplar",
  dependencies=[admin_required]
)
def return_loan_by_copy(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.return_loan_by_copy_id(db, id)
    if not res:
      return ApiResponse.not_found(message="No hay préstamo activo para este exemplar")
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
def expire_overdue_loans(db: Session = Depends(get_db)):
  try:
    count = service.expire_overdue_loans(db)
    return ApiResponse.success(data=count, message=f"{count} préstamos marcados como vencidos")
  except Exception as e:
    return ApiResponse.server_error(str(e))
