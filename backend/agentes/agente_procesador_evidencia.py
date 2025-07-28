# backend/agentes/agente_procesador_evidencia.py

from ..herramientas import herramientas_audio, herramientas_documentos, herramientas_video

def iniciar_procesamiento_de_evidencia(ruta_archivo: str, tipo_contenido: str, id_caso: str) -> dict:
    """
    Decide qué herramienta utilizar para procesar un archivo de evidencia basado en su tipo.

    Este agente actúa como un enrutador. Inspecciona el tipo de contenido del archivo
    (MIME type) y delega el trabajo a la herramienta especializada correspondiente
    (audio, documento, video, etc.).

    Args:
        ruta_archivo (str): La ruta local completa del archivo de evidencia.
        tipo_contenido (str): El tipo MIME del archivo (ej. 'audio/mpeg', 'application/pdf').
        id_caso (str): El ID del caso, necesario para herramientas que guardan archivos temporales.

    Returns:
        dict: Un diccionario con el resultado del procesamiento de la herramienta elegida.
              Normalmente contiene 'texto_extraido' y 'error'.
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
        resultado_procesador = herramientas_documentos.procesar_pdf_con_nougat(ruta_archivo)

    elif 'video' in tipo_contenido:
        print("AGENT-SYSTEM: Decisión: Es un VIDEO. Llamando a la herramienta de procesamiento de video...")
        resultado_procesador = herramientas_video.procesar_video_con_opencv_y_gemini(ruta_archivo, id_caso)
        
    else:
        print(f"AGENT-SYSTEM: Decisión: Tipo de archivo '{tipo_contenido}' no soportado. Usando simulación de respaldo.")
        resultado_procesador = herramientas_documentos.procesar_documento_simulado(ruta_archivo)
    
    texto_resultado = str(resultado_procesador.get("texto_extraido", ""))
    print(f"AGENT-SYSTEM: Resultado del procesamiento: '{texto_resultado[:80]}...'")
    print("==================================================\n")

    return resultado_procesador