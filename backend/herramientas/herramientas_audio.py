# backend/herramientas/herramientas_audio.py

# Importamos la librería que acabamos de instalar
import whisper

def procesar_audio_con_whisper(ruta_archivo: str) -> str:
    """
    Procesa un archivo de audio para transcribir su contenido a texto.
    
    Utiliza el modelo "base" de Whisper, que es multilingüe y eficiente.
    
    Args:
        ruta_archivo (str): La ruta local del archivo de audio a procesar.

    Returns:
        str: El texto transcrito del audio.
    """
    print(f"      TOOL-SYSTEM: -> Herramienta 'procesar_audio_con_whisper' activada para {ruta_archivo}")
    
    try:
        # 1. Cargamos el modelo. "base" es un buen equilibrio entre velocidad y precisión.
        print("      TOOL-SYSTEM: -> Cargando modelo Whisper (esto puede tardar la primera vez)...")
        modelo = whisper.load_model("base")
        
        # 2. Realizamos la transcripción
        print("      TOOL-SYSTEM: -> Transcribiendo audio...")
        resultado = modelo.transcribe(ruta_archivo, fp16=False) # fp16=False es más compatible con CPU
        
        texto_transcrito = resultado["text"]
        
        print("      TOOL-SYSTEM: -> Transcripción completada.")
        return texto_transcrito
        
    except Exception as e:
        print(f"      TOOL-SYSTEM: -> ERROR al procesar el audio: {e}")
        return "Error durante la transcripción del audio."