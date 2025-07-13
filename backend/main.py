# backend/main.py

from fastapi import FastAPI
# ¡NUEVA IMPORTACIÓN!
from fastapi.middleware.cors import CORSMiddleware
from .api import enrutador_principal

aplicacion = FastAPI(
    title="API del Asistente Legal Multimodal",
    description="Proyecto de grado para gestionar y analizar evidencia legal con agentes de IA.",
    version="0.1.0",
)

# ====================================================================
#           CONFIGURACIÓN DE CORS
# ====================================================================
# Lista de orígenes permitidos (nuestra app de React)
origenes_permitidos = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

aplicacion.add_middleware(
    CORSMiddleware,
    allow_origins=origenes_permitidos,
    allow_credentials=True,
    allow_methods=["*"], # Permitimos todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permitimos todos los headers
)
# ====================================================================

aplicacion.include_router(enrutador_principal.router)