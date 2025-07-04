# backend_api/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Definimos la Base aquí, de forma centralizada.
#    Todos los modelos de la aplicación la importarán desde aquí.
Base = declarative_base()

DATABASE_URL = "sqlite:///./fitai.db"
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Añadimos la función get_db que faltaba.
#    Esta es la dependencia que usarán nuestros endpoints.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
