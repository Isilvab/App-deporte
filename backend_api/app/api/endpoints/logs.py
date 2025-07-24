# backend_api/app/api/endpoints/logs.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importaciones de nuestro proyecto
from app.database import get_db
from app.schemas import workout_schema
from app.crud import workout_crud
from app.models import user_model
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/history", response_model=List[workout_schema.WorkoutLogWithName])
def read_user_workout_history(
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    """
    Obtiene el historial de entrenamientos del usuario con los nombres de las rutinas.
    """
    return workout_crud.get_logs_with_workout_names(db=db, user_id=current_user.id)

# --- ¡NUEVO ENDPOINT! ---
@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    """
    Elimina un registro específico del historial de un usuario.
    """
    # 1. Buscamos el log en la base de datos.
    db_log = workout_crud.get_log_by_id(db, log_id=log_id)

    # 2. Verificamos si el log existe.
    if not db_log:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    # 3. Verificación de seguridad: Asegurarnos de que el usuario solo pueda borrar sus propios registros.
    if db_log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar este registro")
        
    # 4. Si todo es correcto, lo eliminamos.
    workout_crud.delete_log(db=db, log=db_log)
    
    # FastAPI devolverá una respuesta 204 No Content automáticamente.
