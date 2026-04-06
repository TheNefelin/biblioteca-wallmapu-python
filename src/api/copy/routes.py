from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.shared.dtos import ApiResponse
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from . import dtos, service

admin_or_user_required = Depends(get_current_user(required_roles=[UserRole.ADMIN, UserRole.LECTOR]))
admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(
  prefix="/edition-copy", 
  tags=["edition-copy"], 
)

# -----------------------------------------------------------------
# GET AVAILABLE COPIES BY BOOK ID (for pickup)
@router.get(
  "/book/{book_id}/available",
  response_model=ApiResponse[List[dtos.CopyDTO]],
  status_code=HTTP_200_OK,
  summary="Listar ejemplares disponibles de un libro",
  dependencies=[admin_required]
)
def get_available_copies_by_book(
  book_id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_available_by_book_id(db, book_id)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(message=str(e))


# -----------------------------------------------------------------
# GET ALL COPIES BY BOOK ID WITH AVAILABILITY STATUS
@router.get(
  "/book/{book_id}",
  response_model=ApiResponse[List[dtos.CopyWithAvailabilityDTO]],
  status_code=HTTP_200_OK,
  summary="Listar todos los ejemplares de un libro con estado de disponibilidad"
)
def get_all_copies_by_book(
  book_id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_all_by_book_id_with_availability(db, book_id)
    return ApiResponse.success(data=res)
  except Exception as e:
    return ApiResponse.server_error(message=str(e))

# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/", 
  response_model=ApiResponse[List[dtos.CopyDTO]],
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
  response_model=ApiResponse[dtos.CopyDTO],
  status_code=HTTP_200_OK
)
def get_all_copy(
  id: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_by_id(id, db)

    if not res:
      return ApiResponse.not_found()

    return ApiResponse.success(data=res)    
  except Exception as e:
    return ApiResponse.server_error(message=str(e))

# -----------------------------------------------------------------
# GET BY EDITION ID
@router.get(
  "/edition/{id_edition}", 
  response_model=ApiResponse[List[dtos.CopyDTO]],
  status_code=HTTP_200_OK
)
def get_all_copy(
  id_edition: int,
  db: Session = Depends(get_db)
):
  try:
    res = service.get_by_edition_id(id_edition, db)
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
    if copy.status_id == 0:
      return ApiResponse.bad_request(message="El estado es requerido")      
    
    if not copy.edition_id:
      return ApiResponse.bad_request(message="El edition_id es requerido")      
      
    if not copy.status_id:
      return ApiResponse.bad_request(message="El status_id es requerido")      
          
    res = service.create(copy, db)

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
      
    res = service.update(id, copy, db)
    
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
    res = service.delete(id, db)

    if res is None:
      return ApiResponse.not_found()

    return ApiResponse.success(data=res)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(message=str(e))
