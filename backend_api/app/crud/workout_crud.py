# backend_api/app/crud/workout_crud.py
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.models import workout_model
from app.schemas import workout_schema

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

def create_workout_log(
    db: Session,
    log_data: workout_schema.WorkoutLogCreate,
    user_id: int,
    workout_id: int
) -> workout_model.WorkoutLog:
    db_log = workout_model.WorkoutLog(
        user_id=user_id,
        workout_id=workout_id,
        performance_data=log_data.performance_data,
        duration_seconds=log_data.duration_seconds,
        calories_burned=log_data.calories_burned,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs_with_workout_names(db: Session, user_id: int):
    results = (
        db.query(
            workout_model.WorkoutLog,
            workout_model.Workout.name.label("workout_name")
        )
        .join(workout_model.Workout, workout_model.WorkoutLog.workout_id == workout_model.Workout.id)
        .filter(workout_model.WorkoutLog.user_id == user_id)
        .order_by(workout_model.WorkoutLog.date_completed.desc())
        .all()
    )
    
    logs_with_names = []
    for log, name in results:
        log_data = {
            "id": log.id, "user_id": log.user_id, "workout_id": log.workout_id,
            "date_completed": log.date_completed, "performance_data": log.performance_data,
            "duration_seconds": log.duration_seconds, "calories_burned": log.calories_burned,
            "workout_name": name,
        }
        logs_with_names.append(log_data)
        
    return logs_with_names

def get_log_by_id(db: Session, log_id: int) -> workout_model.WorkoutLog | None:
    return db.query(workout_model.WorkoutLog).filter(workout_model.WorkoutLog.id == log_id).first()

def delete_log(db: Session, log: workout_model.WorkoutLog):
    db.delete(log)
    db.commit()
