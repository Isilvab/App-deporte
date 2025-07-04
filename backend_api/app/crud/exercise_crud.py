# backend_api/app/crud/exercise_crud.py
from sqlalchemy.orm import Session
from typing import List

# Importamos los modelos y esquemas necesarios
from app.models import exercise_model
from app.schemas import exercise_schema

def get_exercise_by_name(db: Session, name: str) -> exercise_model.Exercise | None:
    """
    Busca un ejercicio en la base de datos por su nombre.
    """
    return db.query(exercise_model.Exercise).filter(exercise_model.Exercise.name == name).first()

def get_exercises(db: Session, skip: int = 0, limit: int = 100) -> List[exercise_model.Exercise]:
    """
    Obtiene una lista de todos los ejercicios, con paginación.
    """
    return db.query(exercise_model.Exercise).offset(skip).limit(limit).all()

def create_exercise(db: Session, exercise: exercise_schema.ExerciseCreate, creator_id: int) -> exercise_model.Exercise:
    """
    Crea un nuevo ejercicio en la base de datos.
    """
    # Creamos el objeto del modelo de base de datos
    db_exercise = exercise_model.Exercise(
        **exercise.model_dump(),  # Desempaqueta los datos del esquema
        creator_id=creator_id
    )
    
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise
