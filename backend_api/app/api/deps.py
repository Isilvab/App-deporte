# backend_api/app/api/deps.py
# Archivo para gestionar las dependencias reutilizables de la API.
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core import security
from app.crud import user_crud
from app.models import user_model
from app.database import get_db

# ¡VERIFICACIÓN CLAVE!
# La URL aquí DEBE coincidir con el prefijo del router y el path del endpoint en main.py y auth.py
# En nuestro caso: prefix="/auth" y path="/token" -> tokenUrl="/auth/token"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> user_model.User:
    """
    Dependencia que obtiene el usuario actual a partir del token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = security.decode_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = user_crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    
    return user
