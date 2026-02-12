from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from src.api.news_gallery import dtos, repository, service
from src.core.database import get_db
from src.shared.dtos import ApiResponse

router = APIRouter(prefix="/news-gallery", tags=["news-gallery"])

@router.get("/news/{news_id}", response_model=ApiResponse[list[dtos.NewsGalleryDTO]])
def get_by_news_id(news_id: int, db: Session = Depends(get_db)):
  try:
    res = repository.get_by_news_id(news_id, db)
  
    return ApiResponse.success(res)
  except Exception as e:
    return ApiResponse.server_error(str(e))  

@router.post("/news/{news_id}",
  response_model=ApiResponse[list[dtos.NewsGalleryDTO]],
  status_code=status.HTTP_201_CREATED
)
def create_gallery(
  news_id: int,
  files: list[UploadFile] = File(...),
  alts: list[str] = Form(...),
  db: Session = Depends(get_db)
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

@router.delete("/news/{news_id}", response_model=ApiResponse[object])
def get_by_news_id(news_id: int, db: Session = Depends(get_db)):
  try:
    res = service.delete_news_gallery_by_news_id(news_id, db)
  
    return ApiResponse.deleted(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))

@router.delete("/{id}", response_model=ApiResponse[object])
def delete(id: int, db: Session = Depends(get_db)):
  try:
    res = service.delete_news_gallery(id, db)
  
    return ApiResponse.deleted(data=res)
  except Exception as e:
    return ApiResponse.server_error(str(e))