# backend/api/modelos_pydantic.py

from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import Literal

# --- Modelo de Evidencia ---
class Evidencia(BaseModel):
    """
    Modelo que representa una pieza de evidencia asociada a un caso.
    """
    id_evidencia: uuid.UUID = Field(title="ID Único de la Evidencia")
    nombre_archivo: str = Field(title="Nombre original del archivo subido")
    ruta_archivo: str = Field(title="Ruta donde se guardó el archivo en el servidor")
    tipo_contenido: str = Field(title="Tipo MIME del archivo (ej. application/pdf)")
    estado_procesamiento: Literal["pendiente", "en_proceso", "completado", "error"] = Field(
        default="pendiente",
        title="Estado del procesamiento por los agentes"
    )


# --- Modelo para la Creación de un Caso ---
class CasoCreacion(BaseModel):
    """
    Modelo de datos para la creación de un nuevo caso.
    """
    titulo: str = Field(
        ...,
        title="Título del Caso",
        description="Un nombre descriptivo y corto para el caso legal.",
        min_length=5,
        max_length=100,
        examples=["Caso de arrendamiento local 201"]
    )
    resumen: str | None = Field(
        default=None,
        title="Resumen Preliminar del Caso",
        description="Una descripción inicial de los hechos o la situación del caso.",
        max_length=500
    )

# --- Modelo de Caso Completo ---
class Caso(CasoCreacion):
    """
    Modelo completo del Caso, incluyendo datos del sistema y su lista de evidencias.
    """
    id_caso: uuid.UUID
    fecha_creacion: datetime
    # ¡NUEVO! Un caso ahora puede contener una lista de evidencias.
    evidencias: list[Evidencia] = Field(
        default_factory=list, # Por defecto, es una lista vacía.
        title="Lista de evidencias del caso"
    )