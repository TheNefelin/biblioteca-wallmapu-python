
import stat
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, session

from src.api.news_gallery import repository
from src.api.news_gallery.dtos import CreateNewsGalleryDTO, NewsGalleryDTO
from src.core.database import get_db
from src.shared.dtos import ApiResponse

router = APIRouter(prefix="/news-gallery", tags=["news-gallery"])

@router.get("/", response_model=ApiResponse[List[NewsGalleryDTO]])
def get_all(db: Session = Depends(get_db)):
  try:
    res = repository.get_all(db)
    return ApiResponse.success(res)
  except Exception as e:
    return ApiResponse.server_error(str(e)) 

@router.get("/{id}", response_model=ApiResponse[NewsGalleryDTO])
def get_by_id(id: int, db: Session = Depends(get_db)):
  try:
    res = repository.get_by_id(id, db)
    
    if not res:
      return ApiResponse.not_found()

    return ApiResponse.success(res)
  except Exception as e:
    return ApiResponse.server_error(str(e))  
  
@router.get("/by-news/{id}", response_model=ApiResponse[List[NewsGalleryDTO]])
def get_by_news_id(id: int, db: Session = Depends(get_db)):
  try:
    res = repository.get_by_news_id(id, db)
    return ApiResponse.success(res)
  except Exception as e:
    return ApiResponse.server_error(str(e))     

@router.post("/", response_model=ApiResponse[NewsGalleryDTO], status_code=status.HTTP_201_CREATED)
def create(news: CreateNewsGalleryDTO, db: Session = Depends(get_db)):
  try:
    created = repository.create(news, db)

    return ApiResponse.created(created)
  except ValueError as e:
    return ApiResponse.bad_request(message=str(e))
  except Exception as e:
    return ApiResponse.server_error(str(e))