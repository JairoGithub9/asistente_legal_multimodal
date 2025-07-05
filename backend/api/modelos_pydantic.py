# backend/api/modelos_pydantic.py

from pydantic import BaseModel, Field
from datetime import datetime
import uuid

# --- Modelo para la Creación de un Caso (Lo que el usuario nos envía) ---
class CasoCreacion(BaseModel):
    """
    Modelo de datos para la creación de un nuevo caso.
    Define los campos que el usuario debe proporcionar.
    """
    titulo: str = Field(
        ..., # El "..." significa que este campo es obligatorio.
        title="Título del Caso",
        description="Un nombre descriptivo y corto para el caso legal.",
        min_length=5,
        max_length=100,
        examples=["Caso de arrendamiento local 201", "Demanda por incumplimiento de contrato XYZ"]
    )
    resumen: str | None = Field(
        default=None, # El "None" significa que este campo es opcional.
        title="Resumen Preliminar del Caso",
        description="Una descripción inicial de los hechos o la situación del caso.",
        max_length=500,
        examples=["El arrendatario no ha pagado los últimos 3 meses de alquiler."]
    )

# --- Modelo de Caso Completo (Lo que nuestra API devuelve) ---
class Caso(CasoCreacion):
    """
    Modelo completo del Caso, incluyendo los campos que genera el sistema.
    Hereda de CasoCreacion para no repetir los campos "titulo" y "resumen".
    """
    id_caso: uuid.UUID = Field(
        title="ID Único del Caso",
        description="Identificador único universal para el caso, generado por el sistema."
    )
    fecha_creacion: datetime = Field(
        title="Fecha y Hora de Creación",
        description="Momento exacto en que el caso fue registrado en el sistema."
    )