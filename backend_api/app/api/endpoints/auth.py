# backend_api/app/api/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

# Importaciones de nuestro proyecto
from app.database import get_db
from app.crud import user_crud
from app.core import security
from app.core.config import settings

# Creamos un router específico para la autenticación
router = APIRouter()

@router.post("/token", response_model=dict)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    Maneja el inicio de sesión del usuario y devuelve un token de acceso.
    """
    user = user_crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crea el token si las credenciales son correctas
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
