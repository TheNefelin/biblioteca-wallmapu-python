from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse
from . import dtos, repository, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/edition", tags=["edition"])

# -----------------------------------------------------------------
# GET ALL
@router.get("/", response_model=ApiResponse[List[dtos.EditionDetailDTO]], status_code=HTTP_200_OK)
def get_all_edition(db: Session = Depends(get_db)):
  res = service.get_all_editions(db)
  return ApiResponse.success(data=res)
  

# -----------------------------------------------------------------
# GET BY ID
@router.get("/{id}", response_model=ApiResponse[dtos.EditionDetailDTO], status_code=HTTP_200_OK)
def get_edition(id: int, db: Session = Depends(get_db)):
  res = service.get_edition_by_id(id, db)
  if not res:
    return ApiResponse.not_found()
  return ApiResponse.success(data=res)


# -----------------------------------------------------------------
# CREATE
@router.post(
  "/", 
  response_model=ApiResponse[dtos.EditionDTO], 
  status_code=HTTP_201_CREATED,
  dependencies=[admin_required],  
)
def create_edition(item: dtos.CreateEditionDTO, db: Session = Depends(get_db)):
  try:
    res = service.create_edition(item, db)
    return ApiResponse.created(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.internal_error(message=str(e))

# -----------------------------------------------------------------
# UPDATE
@router.put(
  "/{id}", 
  response_model=ApiResponse[dtos.EditionDTO], 
  status_code=HTTP_200_OK,
  dependencies=[admin_required],
)
def update_edition(id: int, item: dtos.UpdateEditionDTO, db: Session = Depends(get_db)):
  if item.id_edition != id:
    return ApiResponse.bad_request(message="El Id no coincide")
  
  try:
    result = service.update_edition(id, item, db)
    if not result:
      return ApiResponse.not_found()
    return ApiResponse.success(data=result)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.internal_error(message=str(e))


# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id}", 
  response_model=ApiResponse[bool], 
  status_code=HTTP_200_OK,
  dependencies=[admin_required],  
)
def delete_edition(id: int, db: Session = Depends(get_db)):
  try:
    res = service.delete_edition_with_image(id, db)
    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.internal_error(message=str(e))
