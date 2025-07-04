# backend_api/app/schemas/workout_schema.py
from pydantic import BaseModel
from typing import List, Optional
import datetime

# Importamos los esquemas que ya teníamos para poder anidarlos
from .exercise_schema import Exercise

# --- Esquemas para WorkoutExercise (el vínculo entre rutina y ejercicio) ---

class WorkoutExerciseBase(BaseModel):
    exercise_id: int
    sets: int
    reps: int
    weight_kg: Optional[int] = None
    rest_period_seconds: Optional[int] = None

class WorkoutExerciseCreate(WorkoutExerciseBase):
    pass

class WorkoutExercise(WorkoutExerciseBase):
    id: int
    # Al leer un WorkoutExercise, queremos ver los detalles completos del ejercicio.
    exercise: Exercise

    class Config:
        from_attributes = True


# --- Esquemas para Workout (la rutina completa) ---

class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    # Al crear una rutina, esperamos recibir una lista de los ejercicios que la componen.
    exercises: List[WorkoutExerciseCreate]

class Workout(WorkoutBase):
    id: int
    owner_id: int
    # Al leer una rutina, devolvemos la lista completa de sus ejercicios.
    exercises: List[WorkoutExercise] = []

    class Config:
        from_attributes = True


# --- Esquemas para WorkoutLog (el diario de entrenamiento) ---

class WorkoutLogBase(BaseModel):
    workout_id: Optional[int] = None
    # 'performance_data' será un objeto JSON flexible para guardar los detalles.
    performance_data: dict 

class WorkoutLogCreate(WorkoutLogBase):
    pass

class WorkoutLog(WorkoutLogBase):
    id: int
    user_id: int
    date_completed: datetime.datetime

    class Config:
        from_attributes = True
# Al final de app/schemas/workout_schema.py
class WorkoutLogWithName(WorkoutLog):
    workout_name: str
    
# Al final de app/schemas/workout_schema.py

# Nuevo esquema para actualizar una rutina existente
class WorkoutUpdate(WorkoutCreate):
    pass