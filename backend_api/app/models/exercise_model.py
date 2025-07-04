# backend_api/app/models/exercise_model.py
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

# ¡CAMBIO IMPORTANTE! Importamos la Base centralizada desde database.py
from app.database import Base

class MuscleGroup(str, enum.Enum):
    CHEST = "Pecho"
    BACK = "Espalda"
    LEGS = "Piernas"
    SHOULDERS = "Hombros"
    BICEPS = "Bíceps"
    TRICEPS = "Tríceps"
    ABS = "Abdominales"
    CARDIO = "Cardio"
    FULL_BODY = "Cuerpo Completo"

class Equipment(str, enum.Enum):
    BODYWEIGHT = "Peso Corporal"
    DUMBBELLS = "Mancuernas"
    BARBELL = "Barra"
    KETTLEBELL = "Kettlebell"
    BANDS = "Bandas de Resistencia"
    MACHINE = "Máquina"
    CABLE = "Polea"

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    description = Column(String, nullable=True)
    muscle_group = Column(Enum(MuscleGroup), nullable=False)
    equipment = Column(Enum(Equipment), nullable=False)
    video_url = Column(String, nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    creator = relationship("User")
