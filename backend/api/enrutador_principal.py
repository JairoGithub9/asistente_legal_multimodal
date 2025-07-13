# backend/api/enrutador_principal.py

from fastapi import APIRouter, HTTPException, File, UploadFile
import shutil
from pathlib import Path
from datetime import datetime
import uuid

# ¡CORREGIDO! Importamos todo lo necesario en líneas más limpias.
from .modelos_pydantic import Caso, CasoCreacion, Evidencia
from ..agentes import agente_procesador_evidencia, agente_investigador_analista, agente_sintetizador_estrategico

router = APIRouter(
    tags=["Casos"],
)

db_casos: dict[str, Caso] = {}

@router.get("/", include_in_schema=False)
def leer_raiz():
    return {"mensaje": "Bienvenido al Asistente Legal Multimodal."}


@router.post("/casos", response_model=Caso, status_code=201)
def crear_caso(caso_a_crear: CasoCreacion):
    id_generado = uuid.uuid4()
    nuevo_caso = Caso(
        id_caso=id_generado,
        fecha_creacion=datetime.now(),
        **caso_a_crear.model_dump()
    )
    db_casos[str(id_generado)] = nuevo_caso
    return nuevo_caso


@router.get("/casos/{id_caso}", response_model=Caso)
def obtener_caso(id_caso: str):
    if id_caso not in db_casos:
        raise HTTPException(status_code=404, detail="El caso no fue encontrado")
    return db_casos[id_caso]

@router.get("/casos", response_model=list[Caso])
def listar_casos():
    """
    Devuelve una lista de todos los casos actualmente en memoria.
    """
    return list(db_casos.values())


@router.post("/casos/{id_caso}/evidencia", response_model=Caso)
def subir_evidencia(id_caso: str, archivo: UploadFile = File(...)):
    caso_actual = db_casos.get(id_caso)
    if not caso_actual:
        raise HTTPException(status_code=404, detail="El caso no fue encontrado")

    ruta_guardado_caso = Path("archivos_subidos") / id_caso
    ruta_guardado_caso.mkdir(parents=True, exist_ok=True)
    ruta_archivo_final = ruta_guardado_caso / archivo.filename
    try:
        with open(ruta_archivo_final, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)
    finally:
        archivo.file.close()

    nueva_evidencia = Evidencia(
        id_evidencia=uuid.uuid4(),
        nombre_archivo=archivo.filename,
        ruta_archivo=str(ruta_archivo_final),
        tipo_contenido=archivo.content_type,
        estado_procesamiento="en_proceso"
    )
    
    # --- LLAMADA AL AGENTE 1 ---
    resultado_procesador = agente_procesador_evidencia.iniciar_procesamiento_de_evidencia(
        ruta_archivo=str(ruta_archivo_final),
        tipo_contenido=archivo.content_type
    )
    
    nueva_evidencia.texto_extraido = resultado_procesador.get("texto_extraido")

    # --- LLAMADA AL AGENTE 2 Y 3 (SI HAY TEXTO) ---
    if nueva_evidencia.texto_extraido:
        # Primero, el analista hace su trabajo
        resultado_analista = agente_investigador_analista.analizar_texto_extraido(
            texto=nueva_evidencia.texto_extraido
        )
        nueva_evidencia.entidades_extraidas = resultado_analista.get("entidades")
        nueva_evidencia.informacion_recuperada = resultado_analista.get("informacion_recuperada")

        # ¡CORREGIDO! Este "if" ahora está DENTRO del "if" anterior.
        # Solo si el analista tuvo éxito, llamamos al sintetizador.
        if nueva_evidencia.entidades_extraidas and nueva_evidencia.informacion_recuperada:
            resultado_sintetizador = agente_sintetizador_estrategico.generar_estrategia(
                texto_original=nueva_evidencia.texto_extraido,
                entidades=nueva_evidencia.entidades_extraidas,
                informacion_recuperada=nueva_evidencia.informacion_recuperada
            )
            nueva_evidencia.borrador_estrategia = resultado_sintetizador.get("borrador_estrategia")    

    # Actualizamos el estado final
    nueva_evidencia.estado_procesamiento = "completado" if nueva_evidencia.texto_extraido else "error"
    
    caso_actual.evidencias.append(nueva_evidencia)

    return caso_actual