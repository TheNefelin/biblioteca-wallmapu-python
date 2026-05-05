from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.shared.dtos import ApiResponse
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from . import dtos, service, schema

admin_or_user_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))
admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/copy", 
  tags=["copy"], 
)


# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/", 
  response_model=ApiResponse[List[dtos.CopyWithStatusDTO]],
  status_code=HTTP_200_OK
)
def get_all_copy(db: Session = Depends(get_db)):
  try:
    res = service.get_all(db)
    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# GET BY ID
@router.get(
  "/{id}", 
  response_model=ApiResponse[dtos.CopyWithStatusDTO],
  status_code=HTTP_200_OK
)
def get_copy_by_id(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_by_id(db, id)

    if not res:
      return ApiResponse.not_found()

    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# GET BY EDITION ID
@router.get(
  "/edition/{id_edition}", 
  response_model=ApiResponse[List[dtos.CopyWithStatusDTO]],
  status_code=HTTP_200_OK
)
def get_all_copy_by_edition_id(
  id_edition: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_by_edition_id(db, id_edition)
    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# CREATE
@router.post(
  "/",
  response_model=ApiResponse[dtos.CopyDTO], 
  status_code=HTTP_201_CREATED,
)
def create_copy(
  copy: dtos.CreateCopyDTO, 
  db: Session = Depends(get_db)
):
  try:
    if not copy.edition_id:
      return ApiResponse.bad_request(message="El edition_id es requerido")    
    if not copy.copy_number > 0:
      return ApiResponse.bad_request(message="El numero de copia debe ser mayor a 0")      
          
    res = service.create(db, copy)

    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# UPDATE
@router.put(
  "/{id}",
  response_model=ApiResponse[dtos.CopyDTO], 
  status_code=HTTP_200_OK,
)
def update_copy(
  id: int, 
  copy: dtos.UpdateCopyDTO, 
  db: Session = Depends(get_db)
):
  try:
    if copy.id_copy != id:
      return ApiResponse.bad_request(message="El Id no coincide")

    if not copy.edition_id:
      return ApiResponse.bad_request(message="El edition_id es requerido")      
      
    if not copy.status_id:
      return ApiResponse.bad_request(message="El status_id es requerido")      
      
    res = service.update(db, id, copy)
    
    if not res:
      return ApiResponse.not_found()

    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/{id}",
  response_model=ApiResponse[bool],
  status_code=HTTP_200_OK,
)
def delete_copy(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.delete(db, id)

    if res is None:
      return ApiResponse.not_found()

    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# GET ALL COPIES BY BOOK ID WITH AVAILABILITY STATUS
@router.get(
  "/book/{id_book}/available",
  response_model=ApiResponse[list[schema.CopyAvailabilityDTO]],
  status_code=HTTP_200_OK,
  summary="Listar todos los ejemplares de un libro con estado de disponibilidad"
)
def get_all_copies_by_book(
  id_book: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_all_availability_copies_by_book(db, id_book)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


