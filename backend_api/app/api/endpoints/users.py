# backend_api/app/api/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

# Importaciones de nuestro proyecto
from app.database import get_db
from app.schemas import user_schema
from app.crud import user_crud
from app.models import user_model
from app.api.deps import get_current_user

# Creamos un router específico para los usuarios
router = APIRouter()

@router.post("/", response_model=user_schema.User)
def create_new_user(
    user: user_schema.UserCreate, 
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo usuario en el sistema.
    Este es el endpoint que la pantalla de registro utilizará.
    """
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado.")
    
    return user_crud.create_user(db=db, user=user)

@router.get("/me/", response_model=user_schema.User)
def read_users_me(
    current_user: user_model.User = Depends(get_current_user)
):
    """
    Obtiene la información del perfil del usuario actualmente autenticado.
    """
    return current_user
