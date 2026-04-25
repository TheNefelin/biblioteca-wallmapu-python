from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/loan-policies",
  tags=["loan-policies"],
)

@router.get(
  "/",
  response_model=ApiResponse[List[dtos.LoanPolicyDTO]],
  status_code=HTTP_200_OK,
)
def get_all_policies(db: Session = Depends(get_db)):
  try:
    res = service.get_all(db)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.get(
  "/{id}",
  response_model=ApiResponse[dtos.LoanPolicyDTO],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def get_policy_by_id(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_by_id(db, id)
    if not res:
      return ApiResponse.not_found(message="Política no encontrada")
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.post(
  "/",
  response_model=ApiResponse[dtos.LoanPolicyDTO],
  status_code=HTTP_201_CREATED,
  dependencies=[admin_required]
)
def create_policy(
  dto: dtos.CreateLoanPolicyDTO,
  db: Session = Depends(get_db)
):
  try:
    res = service.create(db, dto)
    return ApiResponse.created(data=res, message="Política creada exitosamente")
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.put(
  "/{id}",
  response_model=ApiResponse[dtos.LoanPolicyDTO],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def update_policy(
  id: int,
  dto: dtos.UpdateLoanPolicyDTO,
  db: Session = Depends(get_db)
):
  try:
    res = service.update(db, id, dto)
    if not res:
      return ApiResponse.not_found(message="Política no encontrada")
    return ApiResponse.updated(data=res, message="Política actualizada")
  except Exception as e:
    return ApiResponse.server_error(str(e))


@router.delete(
  "/{id}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
  dependencies=[admin_required]
)
def delete_policy(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.delete(db, id)
    if res is None:
      return ApiResponse.not_found(message="Política no encontrada")
    return ApiResponse.success(data=res, message="Política eliminada")
  except Exception as e:
    return ApiResponse.server_error(str(e))
