# backend_api/app/crud/workout_crud.py
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.models import workout_model
from app.schemas import workout_schema

# ... (create_workout, get_workouts_by_owner, get_workout, create_workout_log, get_logs_with_workout_names sin cambios) ...
def create_workout(db: Session, workout: workout_schema.WorkoutCreate, owner_id: int) -> workout_model.Workout:
    db_workout = workout_model.Workout(name=workout.name, description=workout.description, owner_id=owner_id)
    db.add(db_workout)
    db.flush()
    for exercise_in in workout.exercises:
        db_workout_exercise = workout_model.WorkoutExercise(**exercise_in.model_dump(), workout_id=db_workout.id)
        db.add(db_workout_exercise)
    db.commit()
    db.refresh(db_workout)
    return db_workout

def get_workouts_by_owner(db: Session, owner_id: int) -> List[workout_model.Workout]:
    return db.query(workout_model.Workout).filter(workout_model.Workout.owner_id == owner_id).all()

def get_workout(db: Session, workout_id: int) -> workout_model.Workout | None:
    return db.query(workout_model.Workout).options(joinedload(workout_model.Workout.exercises).joinedload(workout_model.WorkoutExercise.exercise)).filter(workout_model.Workout.id == workout_id).first()

def create_workout_log(db: Session, log_data: workout_schema.WorkoutLogCreate, user_id: int, workout_id: int) -> workout_model.WorkoutLog:
    db_log = workout_model.WorkoutLog(user_id=user_id, workout_id=workout_id, performance_data=log_data.performance_data)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs_with_workout_names(db: Session, user_id: int):
    results = (db.query(workout_model.WorkoutLog, workout_model.Workout.name.label("workout_name")).join(workout_model.Workout, workout_model.WorkoutLog.workout_id == workout_model.Workout.id).filter(workout_model.WorkoutLog.user_id == user_id).order_by(workout_model.WorkoutLog.date_completed.desc()).all())
    return [workout_schema.WorkoutLogWithName(id=log.id, workout_id=log.workout_id, date_completed=log.date_completed, performance_data=log.performance_data, user_id=log.user_id, workout_name=name) for log, name in results]

# --- ¡NUEVAS FUNCIONES DE MODIFICACIÓN! ---

def update_workout(db: Session, workout: workout_model.Workout, workout_update: workout_schema.WorkoutUpdate) -> workout_model.Workout:
    """
    Actualiza una rutina existente.
    El método simple es borrar los ejercicios antiguos y crear los nuevos.
    """
    # 1. Actualiza los datos simples de la rutina
    workout.name = workout_update.name
    workout.description = workout_update.description
    
    # 2. Borra los ejercicios antiguos asociados a esta rutina
    db.query(workout_model.WorkoutExercise).filter(workout_model.WorkoutExercise.workout_id == workout.id).delete()
    
    # 3. Crea y añade los nuevos ejercicios
    for exercise_in in workout_update.exercises:
        db_workout_exercise = workout_model.WorkoutExercise(
            **exercise_in.model_dump(),
            workout_id=workout.id
        )
        db.add(db_workout_exercise)
        
    db.commit()
    db.refresh(workout)
    return workout

def delete_workout(db: Session, workout: workout_model.Workout):
    """
    Elimina una rutina de la base de datos.
    """
    db.delete(workout)
    db.commit()
