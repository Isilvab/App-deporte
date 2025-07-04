# backend_api/app/api/endpoints/logs.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# Importaciones de nuestro proyecto
from app.database import get_db
from app.schemas import workout_schema
from app.crud import workout_crud
from app.models import user_model
from app.api.deps import get_current_user

router = APIRouter()

# Este es un nuevo endpoint específico para el historial
@router.get("/history", response_model=List[workout_schema.WorkoutLogWithName])
def read_user_workout_history(
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    """
    Obtiene el historial de entrenamientos del usuario con los nombres de las rutinas.
    """
    return workout_crud.get_logs_with_workout_names(db=db, user_id=current_user.id)
