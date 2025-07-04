# scripts/initial_data.py
import sys
import os
from sqlalchemy.orm import Session

# --- Configuración de la Ruta ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Importaciones de nuestra Aplicación ---
from app.database import SessionLocal, engine, Base

# ¡CAMBIO CLAVE! Importamos AMBOS modelos para que SQLAlchemy los conozca.
from app.models.exercise_model import Exercise, MuscleGroup, Equipment
from app.models import user_model # Esta es la línea que faltaba.

# --- La Lista de Ejercicios a Añadir (sin cambios) ---
INITIAL_EXERCISES = [
    {
        "name": "Sentadilla con Peso Corporal",
        "description": "Un ejercicio fundamental para fortalecer piernas y glúteos. Mantén la espalda recta y baja hasta que tus muslos estén paralelos al suelo.",
        "muscle_group": MuscleGroup.LEGS,
        "equipment": Equipment.BODYWEIGHT,
        "video_url": "https://www.youtube.com/watch?v=aclHkVp_i3M",
    },
    {
        "name": "Flexión de Brazos (Push-up)",
        "description": "Excelente para pecho, hombros y tríceps. Mantén el cuerpo en línea recta desde la cabeza hasta los talones.",
        "muscle_group": MuscleGroup.CHEST,
        "equipment": Equipment.BODYWEIGHT,
        "video_url": "https://www.youtube.com/watch?v=F9FCm_K_P5w",
    },
    {
        "name": "Plancha Abdominal (Plank)",
        "description": "Un ejercicio isométrico clave para el core. Contrae los abdominales y los glúteos para mantener una línea recta.",
        "muscle_group": MuscleGroup.ABS,
        "equipment": Equipment.BODYWEIGHT,
        "video_url": "https://www.youtube.com/watch?v=d_R3s-0b9fU",
    },
    {
        "name": "Zancadas (Lunges)",
        "description": "Trabaja la fuerza y estabilidad de cada pierna de forma individual. Da un paso hacia adelante y baja las caderas hasta que ambas rodillas estén dobladas en un ángulo de 90 grados.",
        "muscle_group": MuscleGroup.LEGS,
        "equipment": Equipment.BODYWEIGHT,
        "video_url": "https://www.youtube.com/watch?v=Mxf4545s4U4",
    },
    {
        "name": "Press de Hombros con Mancuernas",
        "description": "Un ejercicio clave para desarrollar fuerza en los hombros. Empuja las mancuernas hacia arriba hasta que los brazos estén completamente extendidos.",
        "muscle_group": MuscleGroup.SHOULDERS,
        "equipment": Equipment.DUMBBELLS,
        "video_url": "https://www.youtube.com/watch?v=B-aVuyAUYpA",
    },
    {
        "name": "Remo con Mancuerna",
        "description": "Fortalece la espalda y los bíceps. Apoya una rodilla y una mano en un banco, y jala la mancuerna hacia tu costado manteniendo la espalda recta.",
        "muscle_group": MuscleGroup.BACK,
        "equipment": Equipment.DUMBBELLS,
        "video_url": "https://www.youtube.com/watch?v=ro3Mh9o7s_A",
    }
]

def seed_initial_data():
    db: Session = SessionLocal()
    print("Iniciando la carga de datos iniciales...")

    try:
        for exercise_data in INITIAL_EXERCISES:
            existing_exercise = db.query(Exercise).filter(Exercise.name == exercise_data["name"]).first()

            if not existing_exercise:
                # Aquí, al no tener un usuario creador, no asignamos creator_id.
                # Será nulo por defecto, como lo definimos en el modelo.
                new_exercise = Exercise(**exercise_data)
                db.add(new_exercise)
                print(f"  -> Añadiendo ejercicio: '{exercise_data['name']}'")
            else:
                print(f"  -> Saltando ejercicio (ya existe): '{exercise_data['name']}'")
        
        db.commit()
        print("\n¡Carga de datos iniciales completada con éxito!")

    finally:
        db.close()

if __name__ == "__main__":
    print("Creando tablas si no existen...")
    # Le decimos a la Base que cree las tablas. Como hemos importado ambos modelos,
    # sabe que debe crear 'users' y 'exercises'.
    Base.metadata.create_all(bind=engine)
    seed_initial_data()
