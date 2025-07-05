# Importamos la clase FastAPI desde la librería fastapi
from fastapi import FastAPI

# Creamos una "instancia" de la aplicación.
# La variable "aplicacion" será nuestro punto de referencia principal.
aplicacion = FastAPI(
    title="API del Asistente Legal Multimodal",
    description="Proyecto de grado para gestionar y analizar evidencia legal con agentes de IA.",
    version="0.1.0",
)

# Este es nuestro primer "endpoint" o "ruta".
# Le decimos a FastAPI que cuando alguien visite la raíz "/" de nuestra API,
# debe ejecutar la función que está justo debajo.
@aplicacion.get("/")
def leer_raiz():
    """
    Endpoint principal que devuelve un saludo de bienvenida.
    """
    return {"mensaje": "Bienvenido al Asistente Legal Multimodal. El servidor está funcionando."}