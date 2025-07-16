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
    id_evidencia: uuid.UUID
    nombre_archivo: str
    ruta_archivo: str
    tipo_contenido: str
    estado_procesamiento: Literal["pendiente", "en_proceso", "completado", "error"] = "pendiente"
    # ¡NUEVO CAMPO!
    texto_extraido: str | None = Field(
        default=None,
        title="Contenido textual extraído de la evidencia"
        
    )
     # ¡NUEVO CAMPO!
    entidades_extraidas: list[dict] | None = Field(
        default=None,
        title="Lista de entidades clave extraídas del texto"
    )
    informacion_recuperada: list[str] | None = Field(
        default=None,
        title="Lista de textos relevantes recuperados de la base de conocimiento"
    )
    borrador_estrategia: str | None = Field(
        default=None,
        title="Borrador de la estrategia o síntesis generada"
    )
    verificacion_calidad: dict | None = Field(
        default=None,
        title="Veredicto del Agente Guardián de Calidad"
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