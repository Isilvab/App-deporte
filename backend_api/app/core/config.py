# backend_api/app/core/config.py
# Este archivo centraliza la configuración de la aplicación.

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configuraciones de la aplicación leídas desde variables de entorno.
    """
    # Clave secreta para firmar los tokens JWT.
    # ¡MUY IMPORTANTE! En un entorno de producción real, este valor
    # debería ser mucho más complejo y leerse desde una variable de entorno segura,
    # no estar escrito directamente aquí. Para nuestro desarrollo, está bien.
    SECRET_KEY: str = "una-clave-secreta-muy-dificil-de-adivinar-0987654321"

    # Algoritmo usado para firmar los tokens. HS256 es el estándar.
    ALGORITHM: str = "HS256"

    # Tiempo de expiración del token de acceso en minutos.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 # El token será válido por 30 minutos

# Creamos una instancia de las configuraciones para poder usarla en otras partes de la app.
settings = Settings()
