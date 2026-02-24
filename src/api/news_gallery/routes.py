from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from src.core.jwt_service import get_current_user
from src.core.roles import UserRole
from src.core.database import get_db
from src.shared.dtos import ApiResponse
from . import dtos, repository, service

admin_required = Depends(get_current_user(required_roles=[UserRole.ADMIN]))

router = APIRouter(prefix="/news-gallery", tags=["news-gallery"])

# -----------------------------------------------------------------
# GET ALL
@router.get(
  "/news/{news_id}", 
  response_model=ApiResponse[list[dtos.NewsGalleryDTO]],
  status_code=HTTP_200_OK
)
def get_by_news_id(news_id: int, db: Session = Depends(get_db)):
  try:
    res = repository.get_by_news_id(news_id, db)
  
    return ApiResponse.success(res)
  except Exception as e:
    return ApiResponse.server_error(str(e))  

# -----------------------------------------------------------------
# CREATE
@router.post(
  "/news/{news_id}",
  response_model=ApiResponse[list[dtos.NewsGalleryDTO]],
  status_code=status.HTTP_201_CREATED
)
def create_gallery(
  news_id: int,
  files: list[UploadFile] = File(...),
  alts: list[str] = Form(...),
  db: Session = Depends(get_db),
  current_user: dict = admin_required
):
  # 🔥 normalización
  if len(alts) == 1 and "," in alts[0]:
    alts = [a.strip() for a in alts[0].split(",")]

  if len(files) != len(alts):
    return ApiResponse.bad_request("La cantidad de imágenes y textos alt no coincide")

  if len(files) > 3:
    return ApiResponse.bad_request("Solo se permiten hasta 3 imágenes")

  try:
    result = service.create_news_gallery_with_images(
      news_id=news_id,
      files=files,
      alts=alts,
      db=db
    )
      
    return ApiResponse.created(result)
  except ValueError as e:
    return ApiResponse.bad_request(str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))

# -----------------------------------------------------------------
# DELETE
@router.delete(
  "/news/{news_id}", 
  response_model=ApiResponse[object],
  status_code=status.HTTP_202_ACCEPTED
)
def delete_by_news_id(news_id: int, db: Session = Depends(get_db), current_user: dict = admin_required):
  try:
    res = service.delete_news_gallery_by_news_id(news_id, db)
  
    return ApiResponse.deleted()
  except Exception as e:
    return ApiResponse.server_error(str(e))

@router.delete("/{id}", response_model=ApiResponse[object])
def delete(id: int, db: Session = Depends(get_db), current_user: dict = admin_required):
  try:
    res = service.delete_news_gallery(id, db)
  
    return ApiResponse.deleted()
  except Exception as e:
    return ApiResponse.server_error(str(e))
