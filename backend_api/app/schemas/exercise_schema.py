# backend_api/app/schemas/exercise_schema.py
from pydantic import BaseModel, HttpUrl
from ..models.exercise_model import MuscleGroup, Equipment

# Esquema base para un ejercicio
class ExerciseBase(BaseModel):
    name: str
    description: str | None = None
    muscle_group: MuscleGroup
    equipment: Equipment
    video_url: HttpUrl | None = None

# Esquema para crear un ejercicio (no necesitamos el creator_id aquí)
class ExerciseCreate(ExerciseBase):
    pass

# Esquema para leer/devolver un ejercicio desde la API
class Exercise(ExerciseBase):
    id: int

    class Config:
        from_attributes = True
