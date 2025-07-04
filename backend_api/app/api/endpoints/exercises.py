# backend_api/app/api/endpoints/exercises.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# Importaciones de nuestro proyecto
from app.database import get_db
from app.schemas import exercise_schema
from app.crud import exercise_crud
from app.models import user_model
from app.api.deps import get_current_user # Crearemos este archivo de dependencias pronto

# Creamos un "router". Es como una mini-aplicación FastAPI.
router = APIRouter()

@router.post("/", response_model=exercise_schema.Exercise)
def create_new_exercise(
    exercise: exercise_schema.ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user) # Protegemos la ruta
):
    """
    Crea un nuevo ejercicio. Solo usuarios autenticados pueden hacerlo.
    """
    db_exercise = exercise_crud.get_exercise_by_name(db, name=exercise.name)
    if db_exercise:
        raise HTTPException(status_code=400, detail="Ya existe un ejercicio con este nombre.")
    
    return exercise_crud.create_exercise(db=db, exercise=exercise, creator_id=current_user.id)

@router.get("/", response_model=List[exercise_schema.Exercise])
def read_exercises(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista de todos los ejercicios. Esta ruta es pública.
    """
    exercises = exercise_crud.get_exercises(db, skip=skip, limit=limit)
    return exercises
