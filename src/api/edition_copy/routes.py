from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.core.database import get_db
from src.shared.dtos import ApiResponse
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from . import dtos, repository

admin_or_user_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(
  prefix="/edition-copy", 
  tags=["edition-copy"], 
  #dependencies=[admin_or_user_required]
)

# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/", 
  response_model=ApiResponse[List[dtos.EditionCopyDTO]],
  status_code=HTTP_200_OK
)
def get_all_copy(db: Session = Depends(get_db)):
  try:
    res = repository.get_all(db)
    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(message=str(e))

# -----------------------------------------------------------------
# GET BY ID
@router.get(
  "/{id}", 
  response_model=ApiResponse[dtos.EditionCopyDTO],
  status_code=HTTP_200_OK
)
def get_all_copy(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = repository.get_by_id(id, db)
    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(message=str(e))

# -----------------------------------------------------------------
# GET BY EDITION ID
@router.get(
  "/edition/{id_edition}", 
  response_model=ApiResponse[List[dtos.EditionCopyDTO]],
  status_code=HTTP_200_OK
)
def get_all_copy(
  id_edition: int,
  db: Session = Depends(get_db)
):
  try:
    res = repository.get_by_edition_id(id_edition, db)
    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
