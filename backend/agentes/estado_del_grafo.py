# backend/agentes/estado_del_grafo.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class EstadoDelGrafo(BaseModel):
    """
    Representa la "hoja de datos" o el estado completo de un caso mientras
    es procesado por nuestro grafo de agentes.

    Este objeto se pasa de un nodo (agente) a otro, y cada agente puede
    leerlo y añadirle información.
    """
    
    # --- Datos Iniciales ---
    # Información que se recibe al inicio del proceso.
    id_caso: str = Field(description="El identificador único del caso.")
    ruta_archivo: str = Field(description="La ruta local del archivo de evidencia subido.")
    tipo_contenido: str = Field(description="El tipo MIME del archivo (ej. 'video/mp4').")

    # --- Resultados de los Agentes ---
    # Cada agente llenará uno o más de estos campos a medida que avanza el grafo.
    
    texto_extraido: Optional[str] = Field(
        default=None, 
        description="El texto transcrito o extraído por el Agente Procesador."
    )
    
    entidades_extraidas: Optional[List[Dict]] = Field(
        default=None, 
        description="Las entidades extraídas por el Agente Investigador/Analista."
    )
    
    informacion_recuperada: Optional[List[str]] = Field(
        default=None, 
        description="La información relevante encontrada en la base de conocimiento por el Agente Investigador/Analista."
    )
    
    borrador_estrategia: Optional[str] = Field(
        default=None, 
        description="El borrador de la estrategia legal generado por el Agente Sintetizador."
    )
    
    verificacion_calidad: Optional[Dict] = Field(
        default=None,
        description="El veredicto del Agente Guardián de Calidad sobre el borrador."
    )

    # --- Control del Flujo ---
    # Campos que nos ayudarán a decidir el camino en el grafo en el futuro.
    
    intentos_correccion: int = Field(
        default=0,
        description="Un contador para saber cuántas veces hemos intentado corregir el borrador."
    )