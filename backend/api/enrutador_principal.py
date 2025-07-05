# backend/api/enrutador_principal.py

from fastapi import APIRouter, HTTPException, File, UploadFile
import shutil
from pathlib import Path
from .modelos_pydantic import Caso, CasoCreacion
from datetime import datetime
import uuid


# Importamos nuestros modelos y el nuevo agente
from .modelos_pydantic import Caso, CasoCreacion, Evidencia
from ..agentes import agente_procesador_evidencia

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


@router.get("/",include_in_schema=False)
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




@router.post("/casos/{id_caso}/evidencia", response_model=Caso)
def subir_evidencia(id_caso: str, archivo: UploadFile = File(...)):
    """
    Sube un archivo de evidencia y activa el agente de procesamiento.
    """
    # 1. Verificamos que el caso exista
    caso_actual = db_casos.get(id_caso)
    if not caso_actual:
        raise HTTPException(status_code=404, detail="El caso no fue encontrado")

    # 2. Guardamos el archivo
    ruta_guardado_caso = Path("archivos_subidos") / id_caso
    ruta_guardado_caso.mkdir(parents=True, exist_ok=True)
    ruta_archivo_final = ruta_guardado_caso / archivo.filename
    try:
        with open(ruta_archivo_final, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)
    finally:
        archivo.file.close()

    # 3. ¡NUEVO! Creamos el registro de la evidencia
    nueva_evidencia = Evidencia(
        id_evidencia=uuid.uuid4(),
        nombre_archivo=archivo.filename,
        ruta_archivo=str(ruta_archivo_final),
        tipo_contenido=archivo.content_type,
    )

    # 4. ¡NUEVO! Añadimos la evidencia al caso
    caso_actual.evidencias.append(nueva_evidencia)

    # 5. ¡NUEVO! ¡Llamamos al Agente!
    agente_procesador_evidencia.iniciar_procesamiento_de_evidencia(
        ruta_archivo=str(ruta_archivo_final),
        tipo_contenido=archivo.content_type
    )

    # 6. Devolvemos el caso completo y actualizado
    return caso_actual