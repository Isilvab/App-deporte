# backend_api/app/core/security.py
from datetime import datetime, timedelta, timezone
from typing import Any, Union

from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel

# Importamos nuestra configuración
from app.core.config import settings

# Contexto de Cifrado para contraseñas (esto ya lo teníamos)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Funciones de Contraseña ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña en texto plano coincide con una hasheada."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Toma una contraseña en texto plano y devuelve su versión hasheada."""
    return pwd_context.hash(password)


# --- NUEVO: Un esquema para el contenido del token ---
class TokenPayload(BaseModel):
    sub: Union[str, int] = None


# --- Funciones para Tokens JWT ---

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Crea un nuevo token de acceso JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# --- ¡NUEVA FUNCIÓN! ---
def decode_token(token: str) -> dict:
    """
    Decodifica un token para extraer su contenido (payload).
    """
    try:
        # Intentamos decodificar el token usando nuestra clave secreta.
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        # Si el token es inválido (firma incorrecta, expirado, etc.), devolvemos un diccionario vacío.
        return {}

