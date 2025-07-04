# backend_api/app/models/user_model.py
import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime

# ¡CAMBIO IMPORTANTE! Importamos la Base centralizada desde database.py
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
