# backend/agentes/agente_procesador_evidencia.py

# Importamos la herramienta que acabamos de crear
from ..herramientas import herramientas_documentos

def iniciar_procesamiento_de_evidencia(ruta_archivo: str, tipo_contenido: str):
    """
    Función de entrada para el Agente Procesador de Evidencia.
    
    Ahora contiene una lógica de decisión para llamar a la herramienta adecuada
    basándose en el tipo de contenido del archivo.
    """
    print("\n" + "="*50)
    print("AGENT-SYSTEM: ¡AGENTE PROCESADOR DE EVIDENCIA ACTIVADO!")
    print(f"AGENT-SYSTEM: Analizando el archivo: {ruta_archivo}")
    print(f"AGENT-SYSTEM: Tipo de contenido detectado: {tipo_contenido}")
    
    texto_extraido = ""

    # =======================================================
    #           AQUÍ ESTÁ EL CEREBRO DEL AGENTE
    # =======================================================
    if "pdf" in tipo_contenido:
        print("AGENT-SYSTEM: Decisión: Es un PDF. Llamando a la herramienta de documentos...")
        texto_extraido = herramientas_documentos.procesar_pdf_con_nougat(ruta_archivo)
    
    elif "audio" in tipo_contenido:
        print("AGENT-SYSTEM: Decisión: Es un AUDIO. (La herramienta de audio aún no está implementada).")
        # texto_extraido = herramientas_audio.procesar_audio_con_whisper(ruta_archivo) # <-- Lógica futura
        
    elif "video" in tipo_contenido:
        print("AGENT-SYSTEM: Decisión: Es un VIDEO. (La herramienta de video aún no está implementada).")
        # texto_extraido = herramientas_video.procesar_video_con_yolo(ruta_archivo) # <-- Lógica futura
        
    else:
        print(f"AGENT-SYSTEM: Decisión: Tipo de archivo '{tipo_contenido}' no soportado todavía.")
    # =======================================================

    print(f"AGENT-SYSTEM: Resultado del procesamiento: '{texto_extraido[:80]}...'") # Mostramos un trozo del resultado
    print("="*50 + "\n")

    return {"estado": "Procesamiento completado", "texto_extraido": texto_extraido}