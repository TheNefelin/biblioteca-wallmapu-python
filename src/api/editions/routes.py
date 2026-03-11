from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse
from . import dtos, repository

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/edition", tags=["edition"])

# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/", 
  response_model=ApiResponse[List[dtos.EditionDTO]],
  status_code=HTTP_200_OK
)
def get_all_edition(db: Session = Depends(get_db)):
  try:
    res = repository.get_all(db)
    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# GET BY ID
@router.get(
  "/{id}", 
  response_model=ApiResponse[dtos.EditionDTO],
  status_code=HTTP_200_OK
)
def get_edition(
  id: int, 
  db: Session = Depends(get_db)
):
  try:
    res = repository.get_by_id(id, db)
    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# CREATE
@router.post(
  "/", 
  response_model=ApiResponse[dtos.EditionDTO],
  status_code=HTTP_201_CREATED
)
def create_edition(
  item: dtos.CreateEditionDTO, 
  db: Session = Depends(get_db)
):
  try:
    res = repository.create(item, db)
    return ApiResponse.created(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))

# -----------------------------------------------------------------
# UPDATE
@router.put(
  "/{id}",
  response_model=ApiResponse[dtos.EditionDTO], 
  status_code=HTTP_200_OK,
)
def update_edition(
  id: int, 
  item: dtos.UpdateEditionDTO, 
  db: Session = Depends(get_db)
):
  try:
    if item.id_edition != id:
      return ApiResponse.bad_request(message="El Id no coincide")

    result = repository.update(item, db)
    
    if not result:
      return ApiResponse.not_found()

    return ApiResponse.success(data=result)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))

# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id}", 
  response_model=ApiResponse[bool], 
  status_code=HTTP_200_OK
)
def delete_edition(
  id: int, 
  db: Session = Depends(get_db), 
):
  try:
    res = repository.delete(id, db)
    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))

