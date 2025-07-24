# backend_api/app/schemas/workout_schema.py
from pydantic import BaseModel
from typing import List, Optional
import datetime
from .exercise_schema import Exercise

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
    exercise: Exercise
    class Config: from_attributes = True

class WorkoutBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    exercises: List[WorkoutExerciseCreate]

class WorkoutUpdate(WorkoutCreate):
    pass

class Workout(WorkoutBase):
    id: int
    owner_id: int
    exercises: List[WorkoutExercise] = []
    class Config: from_attributes = True

# --- ¡ESQUEMAS VERIFICADOS! ---
class WorkoutLogBase(BaseModel):
    performance_data: dict 
    duration_seconds: Optional[int] = None
    calories_burned: Optional[float] = None

class WorkoutLogCreate(WorkoutLogBase):
    pass

class WorkoutLog(WorkoutLogBase):
    id: int
    user_id: int
    workout_id: Optional[int] = None
    date_completed: datetime.datetime
    class Config: from_attributes = True

class WorkoutLogWithName(WorkoutLog):
    workout_name: str
