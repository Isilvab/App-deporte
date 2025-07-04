# backend_api/app/main.py
from fastapi import FastAPI

# Importaciones de nuestro proyecto
from app.database import engine, Base
from app.models import user_model, exercise_model, workout_model
from app.api.endpoints import exercises, auth, workouts, users, logs # ¡Aseguramos que 'logs' esté aquí!

# --- Inicialización ---
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FitAI API",
    description="El cerebro de nuestra aplicación de fitness, impulsado por IA.",
    version="0.9.0",
)

# --- Incluir Routers (El "Mapa" completo y correcto de la API) ---
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(exercises.router, prefix="/exercises", tags=["Exercises"])
app.include_router(workouts.router, prefix="/workouts", tags=["Workouts"])
app.include_router(logs.router, prefix="/logs", tags=["Workout Logs"]) # <-- ¡Esta es la línea clave que soluciona el 404!


@app.get("/")
def read_root():
    """Endpoint raíz para verificar que la API está viva."""
    return {"status": "OK", "message": "¡Bienvenido a la API de FitAI! (Estructura Final con Historial)"}
