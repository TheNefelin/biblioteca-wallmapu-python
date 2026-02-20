from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from src.shared.dtos import ApiResponse
from src.core import jwt_service, roles, database
from . import repository, dtos

admin_required = Depends(jwt_service.get_current_user(required_roles=[roles.UserRole.ADMIN, roles.UserRole.LECTOR]))

router = APIRouter(prefix="/users", tags=["users"], dependencies=[admin_required])

# -----------------------------------------------------------------
# GET ALL
@router.get("/", response_model=ApiResponse[List[dtos.UserDTO]])
def get_all_users(db: Session = Depends(database.get_db)):
  res = repository.get_all(db)
  return ApiResponse.success(data=res)

# -----------------------------------------------------------------
# GET BY ID
@router.get("/{id}", response_model=ApiResponse[dtos.UserDTO])
def get_by_id_user(id: UUID, db: Session = Depends(database.get_db)):
  res = repository.get_by_id(id, db)

  if not res:
    return ApiResponse.not_found(message="Usuario no encontrado")

  return ApiResponse.success(data=res)

# -----------------------------------------------------------------
# UPDATE
@router.put("/{id}", response_model=ApiResponse[dtos.UserDTO])
def update_user(id: UUID, update_dto: dtos.UpdateUserDTO, db: Session = Depends(database.get_db)):
  try:
    updated_dto = repository.update(db, id, update_dto)
    
    if not updated_dto:
      return ApiResponse.not_found(message="Usuario no encontrado")
    
    return ApiResponse.updated(data=updated_dto)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))