# backend/tareas.py

import uuid
from .celery_configuracion import celery_app
from .agentes.orquestador_del_grafo import grafo_compilado
from .base_de_datos import obtener_sesion
from .api.modelos_compartidos import Evidencia
from sqlmodel import Session

@celery_app.task(name="procesar_evidencia_principal")
def procesar_evidencia_tarea(id_evidencia_str: str):
    """
    Tarea de Celery que se ejecuta en segundo plano para procesar un archivo de evidencia.

    Esta función es invocada por el endpoint de la API después de que un archivo
    ha sido subido y se ha creado un registro inicial de Evidencia en la base de datos.
    Se encarga de ejecutar el grafo de agentes, obtener los resultados y actualizar
    el registro de Evidencia correspondiente con el análisis completado.

    Args:
        id_evidencia_str (str): El ID de la evidencia (en formato string) que se debe procesar.
                                Le pasamos un string porque es una mejor práctica para los
                                parámetros de tareas de Celery.
    """
    print(f"INFO: [CELERY-WORKER] Iniciando procesamiento para la evidencia: {id_evidencia_str}")
    
    # Los workers de Celery son procesos separados, por lo que necesitan su propia sesión de BD.
    # Usamos nuestro generador 'obtener_sesion' para manejar esto de forma segura.
    db_session_gen = obtener_sesion()
    sesion: Session = next(db_session_gen)
    
    id_evidencia = uuid.UUID(id_evidencia_str)
    evidencia_db = None # La definimos aquí para poder usarla en el bloque 'except'

    try:
        # 1. Recuperar la evidencia de la base de datos
        evidencia_db = sesion.get(Evidencia, id_evidencia)
        if not evidencia_db:
            print(f"ERROR: [CELERY-WORKER] No se encontró la evidencia con ID: {id_evidencia_str}")
            return # La tarea termina si no hay nada que procesar
            
        # 2. Actualizamos el estado para reflejar que el procesamiento ha comenzado
        evidencia_db.estado_procesamiento = "procesando"
        sesion.add(evidencia_db)
        sesion.commit()
        
        # 3. Preparar el estado inicial para el grafo de agentes
        estado_inicial_del_grafo = {
            "id_caso": str(evidencia_db.id_caso),
            "ruta_archivo": evidencia_db.ruta_archivo,
            "tipo_contenido": evidencia_db.tipo_contenido
        }
        
        # 4. Invocar el grafo de agentes (Esta es la parte que más tiempo consume)
        print(f"INFO: [CELERY-WORKER] Invocando el grafo de agentes para: {evidencia_db.nombre_archivo}")
        estado_final_del_grafo = grafo_compilado.invoke(estado_inicial_del_grafo)
        print(f"INFO: [CELERY-WORKER] El grafo de agentes ha completado el análisis.")

        # 5. Actualizar el registro de la evidencia con los resultados del grafo
        # El método .sqlmodel_update es una forma eficiente de actualizar un objeto 
        # existente con los datos de un diccionario.
        evidencia_db.sqlmodel_update(estado_final_del_grafo)

        # 6. Establecer el estado final del procesamiento
        if estado_final_del_grafo.get("texto_extraido"):
            evidencia_db.estado_procesamiento = "completado"
            print(f"INFO: [CELERY-WORKER] Procesamiento completado con éxito para: {id_evidencia_str}")
        else:
            evidencia_db.estado_procesamiento = "error"
            print(f"ERROR: [CELERY-WORKER] El procesamiento falló (no se extrajo texto) para: {id_evidencia_str}")
            
        sesion.add(evidencia_db)
        sesion.commit()

    except Exception as e:
        # Si ocurre cualquier error inesperado durante el proceso, lo capturamos
        print(f"ERROR-CRITICO: [CELERY-WORKER] Ocurrió una excepción procesando {id_evidencia_str}: {e}")
        # Intentamos actualizar el estado de la evidencia a 'error_critico' si es posible
        if evidencia_db:
            evidencia_db.estado_procesamiento = "error_critico"
            sesion.add(evidencia_db)
            sesion.commit()
            
    finally:
        # Es absolutamente crucial cerrar la sesión de la base de datos al final para liberar la conexión.
        sesion.close()
        print(f"INFO: [CELERY-WORKER] Tarea finalizada y sesión de BD cerrada para: {id_evidencia_str}")