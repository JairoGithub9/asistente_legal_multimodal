# backend/api/modelos_compartidos.py

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
import json
from sqlalchemy import Column, Text
from sqlalchemy.types import TypeDecorator

# =================================================================================
# SECCIÓN 1: "TRADUCTOR" PERSONALIZADO PARA LA BASE DE DATOS
# =================================================================================

class JsonType(TypeDecorator):
    """
    Esta es nuestra clase "Traductora". Le enseña a la base de datos
    cómo manejar listas y diccionarios de Python.
    - Cuando guardamos datos (process_bind_param), convierte el objeto de Python en texto JSON.
    - Cuando leemos datos (process_result_value), convierte el texto JSON de vuelta a un objeto de Python.
    """
    impl = Text
    cache_ok = True

    def process_bind_param(self, value: Optional[Any], dialect: Any) -> Optional[str]:
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value: Optional[str], dialect: Any) -> Optional[Any]:
        if value is not None:
            return json.loads(value)
        return None

# =================================================================================
# SECCIÓN 2: MODELOS DE TABLAS DE BASE DE DATOS
# =================================================================================

class Caso(SQLModel, table=True):
    id_caso: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    titulo: str
    resumen: Optional[str] = Field(default=None)
    fecha_creacion: datetime = Field(default_factory=datetime.now)
    evidencias: List["Evidencia"] = Relationship(back_populates="caso")

class Evidencia(SQLModel, table=True):
    id_evidencia: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id_caso: uuid.UUID = Field(foreign_key="caso.id_caso")
    
    nombre_archivo: str
    ruta_archivo: str
    tipo_contenido: str
    estado_procesamiento: str = Field(default="pendiente")
    
    # --- Columnas con nuestro "Traductor" ---
    # En lugar de Text, usamos nuestro JsonType para estas columnas.
    texto_extraido: Optional[str] = Field(default=None, sa_column=Column(Text))
    entidades_extraidas: Optional[List[Dict]] = Field(default=None, sa_column=Column(JsonType))
    informacion_recuperada: Optional[List[str]] = Field(default=None, sa_column=Column(JsonType))
    borrador_estrategia: Optional[str] = Field(default=None, sa_column=Column(Text))
    verificacion_calidad: Optional[Dict] = Field(default=None, sa_column=Column(JsonType))

    caso: "Caso" = Relationship(back_populates="evidencias")

# =================================================================================
# SECCIÓN 3: MODELOS DE LA API (Entrada y Salida)
# =================================================================================

class CasoCreacion(SQLModel):
    titulo: str
    resumen: Optional[str] = None

class EvidenciaLectura(SQLModel):
    id_evidencia: uuid.UUID
    nombre_archivo: str
    ruta_archivo: str
    tipo_contenido: str
    estado_procesamiento: str
    texto_extraido: Optional[str]
    entidades_extraidas: Optional[List[Dict]]
    informacion_recuperada: Optional[List[str]]
    borrador_estrategia: Optional[str]
    verificacion_calidad: Optional[Dict]

class CasoLectura(SQLModel):
    id_caso: uuid.UUID
    titulo: str
    resumen: Optional[str]
    fecha_creacion: datetime

class CasoLecturaConEvidencias(CasoLectura):
    evidencias: List[EvidenciaLectura] = []