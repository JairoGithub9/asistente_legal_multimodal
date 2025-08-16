# backend/api/enrutador_principal.py

from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
import shutil
from pathlib import Path
from datetime import datetime
import uuid
from sqlmodel import Session, select
from ..base_de_datos import obtener_sesion
# ¡Importamos los nuevos modelos, ahora bien estructurados!
from .modelos_compartidos import Caso, CasoCreacion, Evidencia, CasoLecturaConEvidencias
from ..agentes.orquestador_del_grafo import grafo_compilado

router = APIRouter(tags=["Casos"])

@router.post("/casos", response_model=CasoLecturaConEvidencias, status_code=201)
def crear_caso(sesion: Session = Depends(obtener_sesion), caso_a_crear: CasoCreacion = ...):
    nuevo_caso_db = Caso.model_validate(caso_a_crear)
    sesion.add(nuevo_caso_db)
    sesion.commit()
    sesion.refresh(nuevo_caso_db)
    return nuevo_caso_db

@router.get("/casos", response_model=list[CasoLecturaConEvidencias])
def listar_casos(sesion: Session = Depends(obtener_sesion)):
    casos = sesion.exec(select(Caso)).all()
    return casos

@router.get("/casos/{id_caso}", response_model=CasoLecturaConEvidencias)
def obtener_caso(sesion: Session = Depends(obtener_sesion), id_caso: uuid.UUID = ...):
    caso = sesion.get(Caso, id_caso)
    if not caso:
        raise HTTPException(status_code=404, detail="El caso no fue encontrado")
    return caso

@router.post("/casos/{id_caso}/evidencia", response_model=CasoLecturaConEvidencias)
def subir_evidencia(
    sesion: Session = Depends(obtener_sesion),
    id_caso: uuid.UUID = ...,
    archivo: UploadFile = File(...)
):
    caso_actual = sesion.get(Caso, id_caso)
    if not caso_actual:
        raise HTTPException(status_code=404, detail="El caso no fue encontrado")

    # ... (código de guardado de archivo sin cambios) ...
    ruta_guardado_caso = Path("archivos_subidos") / str(id_caso)
    ruta_guardado_caso.mkdir(parents=True, exist_ok=True)
    ruta_archivo_final = ruta_guardado_caso / archivo.filename
    with open(ruta_archivo_final, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    estado_inicial = { "id_caso": str(id_caso), "ruta_archivo": str(ruta_archivo_final), "tipo_contenido": archivo.content_type }
    estado_final = grafo_compilado.invoke(estado_inicial)

    # Creamos el objeto Evidencia a partir del estado final
    dict_evidencia = {**estado_final, "id_caso": id_caso, "nombre_archivo": archivo.filename, "ruta_archivo": str(ruta_archivo_final)}
    nueva_evidencia_db = Evidencia.model_validate(dict_evidencia)
    nueva_evidencia_db.estado_procesamiento = "completado" if estado_final.get("texto_extraido") else "error"
    
    sesion.add(nueva_evidencia_db)
    sesion.commit()
    sesion.refresh(caso_actual)
    
    return caso_actual