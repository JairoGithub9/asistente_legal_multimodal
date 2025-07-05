# backend/main.py

from fastapi import FastAPI
# Importamos el objeto "router" que creamos en el otro archivo
from .api import enrutador_principal

aplicacion = FastAPI(
    title="API del Asistente Legal Multimodal",
    description="Proyecto de grado para gestionar y analizar evidencia legal con agentes de IA.",
    version="0.1.0",
)

# Le decimos a nuestra aplicación principal que use las rutas definidas
# en nuestro enrutador_principal.
aplicacion.include_router(enrutador_principal.router)