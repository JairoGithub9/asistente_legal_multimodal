# backend/api/enrutador_principal.py

from fastapi import APIRouter, HTTPException, File, UploadFile
import shutil
from pathlib import Path
from .modelos_pydantic import Caso, CasoCreacion
from datetime import datetime
import uuid

# Creamos un enrutador
router = APIRouter(
    tags=["Casos"], # Cambiamos la etiqueta a "Casos" para mejor organización
)

# ====================================================================
#           NUESTRA BASE DE DATOS TEMPORAL EN MEMORIA
# ====================================================================
# Un diccionario para almacenar nuestros casos.
# La llave será el id_caso (convertido a string) y el valor será el objeto Caso.
db_casos: dict[str, Caso] = {}
# ====================================================================


@router.get("/")
def leer_raiz():
    """
    Endpoint principal que devuelve un saludo de bienvenida.
    """
    return {"mensaje": "Bienvenido al Asistente Legal Multimodal."}


@router.post("/casos", response_model=Caso, status_code=201)
def crear_caso(caso_a_crear: CasoCreacion):
    """
    Crea un nuevo caso legal en el sistema.
    """
    id_generado = uuid.uuid4()
    nuevo_caso = Caso(
        id_caso=id_generado,
        fecha_creacion=datetime.now(),
        **caso_a_crear.model_dump()
    )
    # Guardamos el nuevo caso en nuestra "base de datos"
    db_casos[str(id_generado)] = nuevo_caso
    print(f"Caso creado y almacenado con ID: {id_generado}")
    print(f"Casos en la DB: {list(db_casos.keys())}") # Para depurar
    return nuevo_caso


@router.get("/casos/{id_caso}", response_model=Caso)
def obtener_caso(id_caso: str):
    """
    Obtiene los detalles de un caso específico por su ID.
    """
    if id_caso not in db_casos:
        # Si el ID no está en nuestro diccionario, lanzamos un error 404
        raise HTTPException(status_code=404, detail="El caso no fue encontrado")
    
    return db_casos[id_caso]




@router.post("/casos/{id_caso}/evidencia")
def subir_evidencia(id_caso: str, archivo: UploadFile = File(...)):
    """
    Sube un archivo de evidencia (PDF, audio, video, etc.) para un caso específico.
    """
    # 1. Verificamos que el caso exista en nuestra "DB"
    if id_caso not in db_casos:
        raise HTTPException(status_code=404, detail="El caso no fue encontrado")

    # 2. Definimos una ruta segura para guardar el archivo
    # Creamos una carpeta por cada caso para mantener el orden
    ruta_guardado_caso = Path("archivos_subidos") / id_caso
    ruta_guardado_caso.mkdir(parents=True, exist_ok=True)
    
    ruta_archivo_final = ruta_guardado_caso / archivo.filename

    # 3. Guardamos el archivo en el disco
    try:
        with open(ruta_archivo_final, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)
        print(f"Archivo '{archivo.filename}' guardado en '{ruta_archivo_final}'")
    finally:
        archivo.file.close()

    # 4. Por ahora, solo devolvemos un mensaje de éxito.
    # Más adelante, aquí iniciaremos el procesamiento con los agentes.
    return {
        "mensaje": f"Archivo '{archivo.filename}' subido con éxito para el caso {id_caso}",
        "tipo_de_contenido": archivo.content_type,
        "ruta_guardada": str(ruta_archivo_final)
    }