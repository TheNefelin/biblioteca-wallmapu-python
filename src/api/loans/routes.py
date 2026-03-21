from typing import List
from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))
user_or_admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(
  prefix="/loans",
  tags=["loans"],
)

@router.get(
  "/",
  response_model=ApiResponse[List[dtos.LoanDetailDTO]],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def get_all_loans(db: Session = Depends(get_db)):
  try:
    res = service.get_all(db)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.get(
  "/user/{user_id}",
  response_model=ApiResponse[List[dtos.LoanDetailDTO]],
  status_code=HTTP_200_OK,
  dependencies=[user_or_admin_required]
)
def get_loans_by_user(
  user_id: str,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_active_by_user_id(db, user_id)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.get(
  "/book/{book_id}",
  response_model=ApiResponse[List[dtos.LoanDetailDTO]],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def get_loans_by_book(
  book_id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_active_by_book_id(db, book_id)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.get(
  "/overdue",
  response_model=ApiResponse[List[dtos.LoanDetailDTO]],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def get_overdue_loans(db: Session = Depends(get_db)):
  try:
    res = service.get_overdue(db)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.get(
  "/{id}",
  response_model=ApiResponse[dtos.LoanDetailDTO],
  status_code=HTTP_200_OK
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


@router.post(
  "/",
  response_model=ApiResponse[dtos.LoanDetailDTO],
  status_code=HTTP_201_CREATED,
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


@router.put(
  "/{id}/return",
  response_model=ApiResponse[dtos.LoanDetailDTO],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def return_loan(
  id: int,
  dto: dtos.ReturnLoanDTO,
  db: Session = Depends(get_db)
):
  try:
    res = service.return_loan(db, id, dto)
    if not res:
      return ApiResponse.not_found(message="Préstamo no encontrado")
    return ApiResponse.success(data=res, message="Devolución registrada")
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.put(
  "/mark-overdue",
  response_model=ApiResponse[int],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def mark_overdue_loans(db: Session = Depends(get_db)):
  try:
    count = service.mark_overdue_loans(db)
    return ApiResponse.success(data=count, message=f"{count} préstamos marcados como vencidos")
  except Exception as e:
    return ApiResponse.server_error(str(e))
