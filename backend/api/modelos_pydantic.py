# backend/api/modelos_pydantic.py

from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import Literal

class Evidencia(BaseModel):
    """
    Define la estructura de un único archivo de evidencia y todos los
    resultados de su análisis por la cadena de agentes.
    """
    id_evidencia: uuid.UUID
    nombre_archivo: str
    ruta_archivo: str
    tipo_contenido: str
    estado_procesamiento: Literal["pendiente", "en_proceso", "completado", "error"] = "pendiente"
    
    # --- Campos llenados por los agentes de IA ---
    texto_extraido: str | None = Field(
        default=None, title="Contenido textual extraído de la evidencia (transcripción, OCR, etc.)"
    )
    entidades_extraidas: list[dict] | None = Field(
        default=None, title="Lista de entidades clave (hechos, fechas, nombres) extraídas del texto"
    )
    informacion_recuperada: list[str] | None = Field(
        default=None, title="Lista de textos relevantes recuperados de la base de conocimiento (RAG)"
    )
    borrador_estrategia: str | None = Field(
        default=None, title="Borrador de la estrategia o síntesis legal generada por la IA"
    )
    
    # ¡AQUÍ ESTÁ LA CORRECCIÓN!
    # Añadimos el campo que el Agente Guardián produce.
    verificacion_calidad: dict | None = Field(
        default=None, title="El veredicto del Agente Guardián sobre la calidad del borrador"
    )


class CasoCreacion(BaseModel):
    """
    Modelo para la creación de un nuevo caso. Contiene solo los datos
    que el usuario proporciona inicialmente.
    """
    titulo: str = Field(..., min_length=3, max_length=100, description="El título principal del caso.")
    resumen: str | None = Field(default=None, max_length=500, description="Un breve resumen o descripción del caso.")


class Caso(CasoCreacion):
    """
    El modelo completo del Caso, incluyendo los campos generados por el sistema
    y la lista de todas las evidencias asociadas.
    """
    id_caso: uuid.UUID
    fecha_creacion: datetime
    evidencias: list[Evidencia] = Field(default_factory=list)