# backend/agentes/nodos_del_grafo.py

from .estado_del_grafo import EstadoDelGrafo
from ..herramientas import herramientas_audio, herramientas_documentos, herramientas_video,herramientas_lenguaje

import time
# =================================================================================
# NODO 1: AGENTE PROCESADOR DE EVIDENCIA
# =================================================================================

def nodo_procesador_evidencia(estado: EstadoDelGrafo) -> dict:
    """
    Este nodo es el primer paso en el grafo. Llama a la herramienta apropiada
    (audio, pdf, video) para extraer el texto de la evidencia.

    Args:
        estado (EstadoDelGrafo): El estado actual del grafo. Debe contener
                                 la ruta_archivo y el tipo_contenido.

    Returns:
        dict: Un diccionario que contiene el campo 'texto_extraido' para
              actualizar el estado del grafo.
    """
    print("\n--- Entrando en el Nodo: Procesador de Evidencia ---")
    
    # Obtenemos la información necesaria del estado actual
    ruta_archivo = estado.ruta_archivo
    tipo_contenido = estado.tipo_contenido
    id_caso = estado.id_caso
    
    resultado_herramienta = {}

    # Lógica de decisión que ya teníamos, pero ahora dentro de un nodo
    if 'audio' in tipo_contenido:
        print("    Decisión: Es un AUDIO. Llamando a la herramienta de transcripción...")
        resultado_herramienta = herramientas_audio.procesar_audio_con_whisper(ruta_archivo)

    elif 'pdf' in tipo_contenido:
        print("    Decisión: Es un PDF. Llamando a la herramienta de procesamiento (Nougat)...")
        resultado_herramienta = herramientas_documentos.procesar_pdf_con_nougat(ruta_archivo)

    elif 'video' in tipo_contenido:
        print("    Decisión: Es un VIDEO. Llamando a la herramienta de procesamiento de video...")
        resultado_herramienta = herramientas_video.procesar_video_con_opencv_y_gemini(ruta_archivo, id_caso)
        
    else:
        print(f"    Decisión: Tipo de archivo '{tipo_contenido}' no soportado. Usando simulación.")
        resultado_herramienta = herramientas_documentos.procesar_documento_simulado(ruta_archivo)
    
    texto_extraido = resultado_herramienta.get("texto_extraido")
    
    if texto_extraido:
        print(f"    Resultado: Texto extraído exitosamente ({len(texto_extraido)} caracteres).")
    else:
        print("    Resultado: No se pudo extraer texto.")

    # El nodo devuelve un diccionario con las claves del estado que quiere modificar.
    return {"texto_extraido": texto_extraido}


# =================================================================================
# NODO 2: AGENTE INVESTIGADOR Y ANALISTA
# =================================================================================

def nodo_investigador_analista(estado: EstadoDelGrafo) -> dict:
    """
    Este nodo toma el texto extraído y realiza la investigación.

    Implementa una pausa inicial para dar un respiro a la API después de
    posibles tareas intensivas del nodo anterior (como el análisis de video).
    """
    print("\n--- Entrando en el Nodo: Investigador y Analista ---")
    
    texto_para_analizar = estado.texto_extraido
    
    if not texto_para_analizar:
        print("    Decisión: No hay texto para analizar. Saltando el nodo.")
        return {}

    # --- ¡CORRECCIÓN ESTRATÉGICA! ---
    # Le damos un respiro a la API antes de empezar a trabajar.
    pausa = 20
    print(f"    Acción: Pausa de {pausa} segundos para estabilizar la conexión con la API...")
    time.sleep(pausa)
    # ----------------------------------

    # 1. Extraer entidades
    print("    Acción: Extrayendo entidades clave del texto...")
    entidades = herramientas_lenguaje.extraer_entidades_con_llm(texto_para_analizar)
    
    if not entidades or "Error" in entidades[0].get("tipo", ""):
        print("    Resultado: No se pudieron extraer entidades.")
        # Devolvemos ambos campos como nulos para evitar errores en cascada
        return {"entidades_extraidas": None, "informacion_recuperada": None}

    print(f"    Resultado: Se extrajeron {len(entidades)} entidades.")

    # 2. Buscar en la base de conocimiento (RAG)
    consulta_rag = " ".join([ent["entidad"] for ent in entidades])
    print(f"    Acción: Buscando en la base de conocimiento con la consulta: '{consulta_rag[:100]}...'")
    
    informacion_recuperada = herramientas_lenguaje.buscar_en_base_de_conocimiento(consulta_rag)
    
    print(f"    Resultado: Se recuperaron {len(informacion_recuperada)} fragmentos de información.")

    return {
        "entidades_extraidas": entidades,
        "informacion_recuperada": informacion_recuperada
    }

# backend/agentes/nodos_del_grafo.py

# (Imports y nodos anteriores van aquí arriba)

# =================================================================================
# NODO 3: AGENTE SINTETIZADOR ESTRATÉGICO
# =================================================================================

def nodo_sintetizador_estrategico(estado: EstadoDelGrafo) -> dict:
    """
    Este nodo compila toda la información para generar un borrador de estrategia.

    VERSIÓN MEJORADA:
    - Ahora revisa si hay un veredicto de calidad previo en el estado.
    - Si el borrador anterior fue rechazado, incorpora las observaciones del
      Guardián en un nuevo prompt para solicitar una versión corregida.
    """
    print("\n--- Entrando en el Nodo: Sintetizador Estratégico ---")

    if not estado.texto_extraido or not estado.entidades_extraidas or not estado.informacion_recuperada:
        print("    Decisión: Faltan datos. No se puede generar la síntesis.")
        return {"borrador_estrategia": "Error: Faltan datos previos."}

    # 1. Preparamos el contexto base (esto no cambia)
    contexto_base = f"""
    **Texto Original de la Evidencia:**
    {estado.texto_extraido}
    **Entidades Clave Identificadas:**
    {estado.entidades_extraidas}
    **Artículos y Leyes Relevantes Recuperados:**
    {estado.informacion_recuperada}
    """
    
    # 2. Lógica para manejar la corrección
    veredicto_previo = estado.verificacion_calidad
    if veredicto_previo and not veredicto_previo.get("verificado"):
        # ¡Estamos en un bucle de corrección!
        print("    Acción: Detectado un rechazo previo. Preparando prompt de corrección.")
        observaciones = veredicto_previo.get("observaciones")
        
        prompt_final = f"""
        Eres un abogado senior y tu borrador anterior fue rechazado por un auditor.
        Tu tarea es generar una NUEVA Y MEJORADA versión del "Borrador de Estrategia Legal Preliminar"
        basándote en el contexto original y corrigiendo OBLIGATORIAMENTE los errores señalados.

        **Observaciones del Auditor (Errores a Corregir):**
        {observaciones}

        **Contexto Original (Úsalo como base):**
        {contexto_base}

        Genera una nueva versión que solucione los problemas mencionados.
        """
    else:
        # Es la primera vez que pasamos por aquí.
        print("    Acción: Primera pasada. Preparando prompt de síntesis inicial.")
        prompt_final = f"""
        Eres un abogado senior y director de un consultorio jurídico en Colombia.
        Tu tarea es revisar el siguiente contexto y redactar un "Borrador de Estrategia Legal Preliminar".
        El borrador debe ser claro, estructurado y profesional, usando Markdown.
        Debes incluir:
        1. Resumen breve del caso.
        2. Fundamento legal principal.
        3. Posibles demandados.
        4. Consideración sobre la competencia del consultorio.
        5. Próximo paso recomendado.

        Contexto para analizar:
        ---
        {contexto_base}
        ---
        """

    # 3. Llamamos a la IA con el prompt adecuado
    print("    Acción: Solicitando la generación del borrador a la IA...")
    borrador_generado = herramientas_lenguaje.generar_sintesis_con_llm(prompt_final)
    
    print("    Resultado: Nueva versión del borrador generada.")

    # Incrementamos el contador de intentos y devolvemos el nuevo borrador
    return {
        "borrador_estrategia": borrador_generado,
        "intentos_correccion": estado.intentos_correccion + 1
    }


# =================================================================================
# NODO 4: AGENTE GUARDIÁN DE CALIDAD
# =================================================================================

def nodo_guardian_calidad(estado: EstadoDelGrafo) -> dict:
    """
    Este nodo revisa el borrador de estrategia para asegurar su calidad y
    coherencia con la evidencia original.

    Args:
        estado (EstadoDelGrafo): El estado actual, que debe contener el borrador
                                 y el contexto original que lo generó.

    Returns:
        dict: Un diccionario con la 'verificacion_calidad' para actualizar el estado.
    """
    print("\n--- Entrando en el Nodo: Guardián de Calidad ---")

    borrador_a_revisar = estado.borrador_estrategia
    
    if not borrador_a_revisar or "Error" in borrador_a_revisar:
        print("    Decisión: No hay un borrador válido para revisar. Saltando el nodo.")
        veredicto = {
            "verificado": False,
            "observaciones": "No se generó un borrador para poder revisar."
        }
        return {"verificacion_calidad": veredicto}

    # 1. Reconstruimos el contexto original que se usó para la síntesis
    contexto_original = f"""
    **Texto Original de la Evidencia:**
    {estado.texto_extraido}

    **Entidades Clave Identificadas:**
    {estado.entidades_extraidas}

    **Artículos y Leyes Relevantes Recuperados de la Base de Conocimiento:**
    {estado.informacion_recuperada}
    """
    print("    Acción: Reconstruyendo contexto para la revisión.")

    # 2. Llamamos a la herramienta de verificación
    print("    Acción: Solicitando la verificación de calidad a la IA...")
    veredicto = herramientas_lenguaje.verificar_calidad_con_llm(
        borrador=borrador_a_revisar,
        contexto_original=contexto_original
    )
    
    print(f"    Resultado: Veredicto de calidad recibido. Verificado: {veredicto.get('verificado')}")

    return {"verificacion_calidad": veredicto}