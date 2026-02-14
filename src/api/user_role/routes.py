from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.shared.dtos import ApiResponse
from src.api.user_role.repository import get_all
from src.api.user_role.dtos import UserRoleDTO
from src.core.database import get_db

router = APIRouter(prefix="/user-role", tags=["user-role"])

# GET ALL
@router.get("/", response_model=ApiResponse[List[UserRoleDTO]])
def get_all_role(db: Session = Depends(get_db)):
  res = get_all(db)
  return ApiResponse.success(data=res)
