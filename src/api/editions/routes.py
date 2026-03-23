from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.core.database import get_db
from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.shared.dtos import ApiResponse, BookPaginationRequestDTO, PaginationResponseDTO
from . import dtos, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/edition", tags=["edition"])


# -----------------------------------------------------------------
# GET ALL
@router.get("/pagination", 
  response_model=ApiResponse[PaginationResponseDTO[List[dtos.EditionDetailDTO]]],  
  status_code=HTTP_200_OK,
)
def get_all_pagination(
  page: int = Query(default=1, ge=1, description="Número de página a mostrar"),
  limit: int = Query(default=10, ge=1, le=100, description="Cantidad de elementos por página"),
  search: Optional[str] = Query(default=None, description="Buscar opcional"),
  id_author: Optional[int] = Query(default=None, description="Buscar por autor opcional"),
  id_editorial: Optional[int] = Query(default=None, description="Buscar por editorial opcional"),
  id_genre: Optional[int] = Query(default=None, description="Buscar por generlo opcional"),   
  db: Session = Depends(get_db)
):
  pagination_request = BookPaginationRequestDTO(
    page=page,
    limit=limit,
    search=search,
    id_author=id_author,
    id_editorial=id_editorial,
    id_genre=id_genre,
  )
  
  pagination_response = service.get_all_pagination(pagination_request, db)
  return ApiResponse.success(pagination_response)
  

# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/", 
  response_model=ApiResponse[List[dtos.EditionDetailDTO]], 
  status_code=HTTP_200_OK,
  #dependencies=[admin_required],
)
def get_all_edition(db: Session = Depends(get_db)):
  res = service.get_all_editions(db)
  return ApiResponse.success(data=res)
  

# -----------------------------------------------------------------
# GET BY ID
@router.get(
  "/{id}", 
  response_model=ApiResponse[dtos.EditionDetailDTO], 
  status_code=HTTP_200_OK,
  dependencies=[admin_required],
)
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
    return ApiResponse.server_error(message=str(e))

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
    return ApiResponse.server_error(message=str(e))


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
    return ApiResponse.server_error(message=str(e))
