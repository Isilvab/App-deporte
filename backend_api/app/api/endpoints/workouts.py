# backend_api/app/api/endpoints/workouts.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import workout_schema
from app.crud import workout_crud
from app.models import user_model
from app.api.deps import get_current_user

router = APIRouter()

# ... (POST / y GET / sin cambios) ...
@router.post("/", response_model=workout_schema.Workout)
def create_user_workout(workout: workout_schema.WorkoutCreate, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    return workout_crud.create_workout(db=db, workout=workout, owner_id=current_user.id)

@router.get("/", response_model=List[workout_schema.Workout])
def read_user_workouts(db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    return workout_crud.get_workouts_by_owner(db=db, owner_id=current_user.id)

@router.get("/{workout_id}", response_model=workout_schema.Workout)
def read_workout(workout_id: int, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    db_workout = workout_crud.get_workout(db, workout_id=workout_id)
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    if db_workout.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para ver esta rutina")
    return db_workout

# --- ¡NUEVOS ENDPOINTS DE MODIFICACIÓN! ---

@router.put("/{workout_id}", response_model=workout_schema.Workout)
def update_user_workout(
    workout_id: int,
    workout_update: workout_schema.WorkoutUpdate,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    db_workout = workout_crud.get_workout(db, workout_id=workout_id)
    if not db_workout:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    if db_workout.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta rutina")
    return workout_crud.update_workout(db=db, workout=db_workout, workout_update=workout_update)

@router.delete("/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    db_workout = workout_crud.get_workout(db, workout_id=workout_id)
    if not db_workout:
        raise HTTPException(status_code=404, detail="Rutina no encontrada")
    if db_workout.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar esta rutina")
    workout_crud.delete_workout(db=db, workout=db_workout)
    return {"ok": True} # Devuelve una respuesta vacía 204

# ... (POST /{workout_id}/log sin cambios) ...
@router.post("/{workout_id}/log", response_model=workout_schema.WorkoutLog)
def log_completed_workout(workout_id: int, log_data: workout_schema.WorkoutLogCreate, db: Session = Depends(get_db), current_user: user_model.User = Depends(get_current_user)):
    return workout_crud.create_workout_log(db=db, log_data=log_data, user_id=current_user.id, workout_id=workout_id)
