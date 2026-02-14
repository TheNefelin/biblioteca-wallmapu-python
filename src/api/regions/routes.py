from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.regions.dtos import RegionDTO
from src.api.regions.repository import get_all
from src.core.database import get_db
from src.shared.dtos import ApiResponse

router = APIRouter(prefix="/region", tags=["region"])

# GET ALL
@router.get("/", response_model=ApiResponse[List[RegionDTO]])
def get_all_region(db: Session = Depends(get_db)):
  try:
    res = get_all(db)
    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(str(e))
