from typing import Any, Optional
from fastapi import APIRouter, status
from src.api.a01.dtos import ApiResponse, BoricResponse

router = APIRouter(prefix="/boric-ai", tags=["boric-ai"])

@router.post("/", response_model=ApiResponse[BoricResponse], status_code=status.HTTP_200_OK)
def create(item: Optional[Any] = None):
  resp = BoricResponse(
    text="No tengo la cifra exacta",
  )

  return ApiResponse[BoricResponse](
    isSuccess=True,
    statusCode=418,
    message="Ok.. error? 420",
    data=resp
  )
