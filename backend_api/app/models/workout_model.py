# backend_api/app/models/workout_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Float
from sqlalchemy.orm import relationship
import datetime

from app.database import Base

class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")
    exercises = relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")

class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"
    id = Column(Integer, primary_key=True, index=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    sets = Column(Integer)
    reps = Column(Integer)
    weight_kg = Column(Integer, nullable=True)
    rest_period_seconds = Column(Integer, nullable=True)
    workout = relationship("Workout", back_populates="exercises")
    exercise = relationship("Exercise")

class WorkoutLog(Base):
    __tablename__ = "workout_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=True)
    date_completed = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    performance_data = Column(JSON)
    # --- ¡CAMPOS VERIFICADOS! ---
    duration_seconds = Column(Integer, nullable=True)
    calories_burned = Column(Float, nullable=True)
