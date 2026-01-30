from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from src.core.database import get_db
from . import repository, dtos

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[dtos.UserDTO])
def get_all_users(db: Session = Depends(get_db)):
  res = repository.get_all(db)
  return res

@router.get("/{id}", response_model=dtos.UserDTO)
def get_by_id_user(id: UUID, db: Session = Depends(get_db)):
  res = repository.get_by_id(db, id)
  if not res:
    raise HTTPException(status_code=404, detail="Usuario no encontrado")
  return res

@router.post("/", response_model=dtos.UserDTO, status_code=status.HTTP_201_CREATED)
def create_user(user: dtos.CreateUserDTO, db: Session = Depends(get_db)):
  try:
    new_user = repository.create(db, user)
    return new_user
  except ValueError as e:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=str(e)
    )
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Error interno del servidor"
    )
  
@router.put("/{id}", response_model=dtos.UserDTO)
def update_user(id: UUID, user: dtos.UpdateUserDTO, db: Session = Depends(get_db)):
  try:
    updated_user = repository.update(db, id, user)
    
    if not updated_user:
      raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Usuario con id {id} no encontrado"
      )
    
    return updated_user
  except ValueError as e:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail=str(e)
    )
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Error interno del servidor"
    ) 