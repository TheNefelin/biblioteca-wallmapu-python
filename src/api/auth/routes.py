from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.jwt_service import create_access_token
from . import dtos, repository, google_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/google", response_model=dtos.AuthGoogleResponse)
def auth_google(auth_data: dtos.AuthGoogleRequest, db: Session = Depends(get_db)):
  try:
    # 1. Validar Access Token con Google
    google_user = google_service.verify_google_token(auth_data.googleToken)
    
    if not google_user.email_verified:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email no verificado en Google"
      )
    
    # 2. Obtener o crear usuario (sin picture)
    user, is_new = repository.get_or_create_user_from_google(
      db,
      email=google_user.email,
      name=google_user.name,
      google_id=google_user.google_id  # ✅ Sin picture
    )
    
    # 3. Generar JWT de tu backend
    token = create_access_token(user.id_user)
    
    # 4. Verificar si el perfil está completo
    profile_complete = bool(
      user.name and 
      user.lastname and 
      user.rut
    )
    
    # 5. Retornar respuesta (picture viene de Google, no de BD)
    return dtos.AuthGoogleResponse(
      token=token,
      user=dtos.AuthUser(
        id_user=user.id_user,
        email=google_user.email,
        name=user.name,
        picture=google_user.picture,  # ✅ Viene de Google, no de BD
        profileComplete=profile_complete,
        user_role_id=user.user_role_id
      )
    )
    
  except ValueError as e:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail=str(e)
    )
  except Exception as e:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail=f"Error en autenticación: {str(e)}"
    )