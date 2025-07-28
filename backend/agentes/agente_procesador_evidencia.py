from ..herramientas import herramientas_documentos, herramientas_audio

def iniciar_procesamiento_de_evidencia(ruta_archivo: str, tipo_contenido: str) -> dict:
    """
    Decide qué herramienta de procesamiento utilizar basándose en el tipo de contenido
    del archivo de evidencia y la ejecuta.

    Args:
        ruta_archivo (str): La ruta al archivo de evidencia.
        tipo_contenido (str): El tipo MIME del archivo (ej. 'audio/mpeg', 'application/pdf').

    Returns:
        dict: Un diccionario con el resultado del procesamiento. La estructura exacta
              depende de la herramienta que se haya llamado.
    """
    print("\n==================================================")
    print("AGENT-SYSTEM: ¡AGENTE PROCESADOR DE EVIDENCIA ACTIVADO!")
    print(f"AGENT-SYSTEM: Analizando el archivo: {ruta_archivo}")
    print(f"AGENT-SYSTEM: Tipo de contenido detectado: {tipo_contenido}")

    resultado_procesador = {}

    if 'audio' in tipo_contenido:
        print("AGENT-SYSTEM: Decisión: Es un AUDIO. Llamando a la herramienta de transcripción...")
        resultado_procesador = herramientas_audio.procesar_audio_con_whisper(ruta_archivo)

    elif 'pdf' in tipo_contenido:
        print("AGENT-SYSTEM: Decisión: Es un PDF. Llamando a la herramienta de procesamiento de documentos (Nougat)...")
        # Llamamos a la nueva función real para PDFs
        resultado_procesador = herramientas_documentos.procesar_pdf_con_nougat(ruta_archivo)

    else:
        print("AGENT-SYSTEM: Decisión: Tipo de archivo no soportado directamente. Usando simulación...")
        # Como respaldo, usamos la función simulada para otros tipos de documentos
        resultado_procesador = herramientas_documentos.procesar_documento_simulado(ruta_archivo)

    print(f"AGENT-SYSTEM: Resultado del procesamiento: '{str(resultado_procesador.get('texto_extraido'))[:100]}...'")
    print("==================================================\n")
    
    return resultado_procesador