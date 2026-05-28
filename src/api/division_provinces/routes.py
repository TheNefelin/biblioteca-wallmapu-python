from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse
from . import dtos, service

admin_or_user_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))

router = APIRouter(prefix="/division-province", tags=["division-province"], dependencies=[admin_or_user_required])

# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/", 
  response_model=ApiResponse[List[dtos.ProvinceDTO]],
  status_code=HTTP_200_OK,
  summary="Listar provincias",
  description="Obtiene lista completa de provincias ordenada por nombre",
)
def get_all_province(db: Session = Depends(get_db)):
  try:
    res = service.get_all(db)
    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(str(e))
