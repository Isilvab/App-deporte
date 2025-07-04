# backend_api/app/crud/user_crud.py
from sqlalchemy.orm import Session

# Usamos importaciones absolutas para evitar problemas de entorno
from app.models import user_model
from app.schemas import user_schema
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = user_model.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
