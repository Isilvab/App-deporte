# backend_api/app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr
import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime.datetime

    class Config:
        from_attributes = True
