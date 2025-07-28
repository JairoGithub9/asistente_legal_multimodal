import whisper

# Cargamos el modelo una sola vez para eficiencia.
try:
    modelo_whisper = whisper.load_model("base")
    print("TOOL-SETUP: Modelo Whisper cargado correctamente en memoria.")
except Exception as e:
    modelo_whisper = None
    print(f"TOOL-SETUP-ERROR: No se pudo cargar el modelo Whisper. {e}")

def procesar_audio_con_whisper(ruta_archivo: str) -> dict:
    """
    Transcribe un archivo de audio a texto utilizando el modelo Whisper de OpenAI.
    La salida de esta función está estandarizada a un diccionario.

    Args:
        ruta_archivo (str): La ruta completa al archivo de audio a transcribir.

    Returns:
        dict: Un diccionario que contiene el texto transcrito en la clave 'texto_extraido'.
              Si ocurre un error, el valor será None y se añadirá una clave 'error'.
    """
    resultado = {"texto_extraido": None, "error": None}

    if not modelo_whisper:
        error_msg = "El modelo Whisper no está disponible o no se pudo cargar."
        print(f"TOOL-SYSTEM-ERROR: {error_msg}")
        resultado["error"] = error_msg
        return resultado

    try:
        print(f"      TOOL-SYSTEM: -> Herramienta 'procesar_audio_con_whisper' activada para {ruta_archivo}")
        print("      TOOL-SYSTEM: -> Transcribiendo audio con Whisper...")
        
        # Realizamos la transcripción
        transcripcion = modelo_whisper.transcribe(ruta_archivo)
        texto_transcrito = transcripcion["text"]
        
        resultado["texto_extraido"] = texto_transcrito
        print("      TOOL-SYSTEM: -> Transcripción completada.")
        
    except Exception as e:
        error_msg = f"Ocurrió un error inesperado al transcribir el audio: {e}"
        print(f"TOOL-SYSTEM-ERROR: {error_msg}")
        resultado["error"] = error_msg

    return resultado