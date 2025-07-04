# backend_api/app/models/workout_model.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
import datetime

# Importamos la Base centralizada de nuestra aplicación
from app.database import Base

class Workout(Base):
    """
    Representa una rutina de entrenamiento creada por un usuario.
    Ej: "Día de Piernas", "Rutina de Cardio Semanal".
    """
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)

    # Cada rutina pertenece a un usuario.
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")

    # Relación para acceder a los ejercicios de esta rutina.
    exercises = relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")

class WorkoutExercise(Base):
    """
    Tabla de asociación que conecta una Rutina (Workout) con un Ejercicio (Exercise).
    Aquí se definen los detalles de cómo se debe realizar el ejercicio dentro de la rutina.
    """
    __tablename__ = "workout_exercises"

    id = Column(Integer, primary_key=True, index=True)
    
    # Conexión a la rutina y al ejercicio
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))

    # Detalles del ejercicio en la rutina
    sets = Column(Integer) # Número de series
    reps = Column(Integer) # Número de repeticiones por serie
    weight_kg = Column(Integer, nullable=True) # Peso en kg (opcional)
    rest_period_seconds = Column(Integer, nullable=True) # Descanso en segundos
    
    # Relaciones para navegar fácilmente desde aquí
    workout = relationship("Workout", back_populates="exercises")
    exercise = relationship("Exercise")

class WorkoutLog(Base):
    """
    Un registro o "log" de una sesión de entrenamiento completada por un usuario.
    Esta tabla es la fuente de datos MÁS IMPORTANTE para la futura IA.
    """
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # El usuario que completó el entrenamiento
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # La rutina que se realizó (puede ser nulo si fue un entrenamiento libre)
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=True)

    # Fecha en que se completó el entrenamiento
    date_completed = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    # Un campo JSON para guardar los detalles exactos del rendimiento.
    # Ej: {"exercise_id_1": [{"set": 1, "reps": 10, "weight": 50}, ...]}
    performance_data = Column(JSON)
