# backend/herramientas/herramientas_audio.py

import base64
import mimetypes
from pathlib import Path

# ¡LA IMPORTACIÓN CLAVE!
# Importamos el modelo multimodal que ya inicializamos en nuestras herramientas de lenguaje.
# Esto evita tener que cargarlo en memoria dos veces.
from .herramientas_lenguaje import modelo_gemini_flash
from langchain_core.messages import HumanMessage

def transcribir_audio_con_gemini(ruta_archivo_audio: str) -> str:
    """
    Procesa un archivo de audio utilizando el modelo multimodal Gemini 1.5 Flash
    para realizar tanto la transcripción como la diarización (identificación de hablantes).

    Esta función reemplaza completamente el uso de Whisper, alineándose con el requisito
    de utilizar un modelo multimodal nativo para el análisis de audio.

    Args:
        ruta_archivo_audio (str): La ruta al archivo de audio (ej. MP3, WAV, etc.).

    Returns:
        str: Un string con la transcripción formateada, incluyendo la identificación
             de cada hablante. Retorna un mensaje de error si el procesamiento falla.
    """
    print(f"      TOOL-SYSTEM: -> Herramienta NATIVA MULTIMODAL (Gemini) activada para {ruta_archivo_audio}")

    try:
        ruta = Path(ruta_archivo_audio)
        if not ruta.is_file():
            return "Error: El archivo de audio no fue encontrado en la ruta especificada."

        with open(ruta, "rb") as archivo_audio:
            audio_bytes = archivo_audio.read()
        audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

        tipo_mime, _ = mimetypes.guess_type(ruta)
        if not tipo_mime:
            tipo_mime = "application/octet-stream"

        mensaje_multimodal = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": """
                    Eres un asistente legal experto en el análisis de evidencia de audio.
                    Tu tarea es procesar el archivo de audio adjunto y generar una transcripción con diarización precisa.
                    
                    Requisitos estrictos de la salida:
                    1. Identifica a cada hablante distinto y asígnale un alias numérico (ej. "Hablante 1", "Hablante 2").
                    2. Formatea cada segmento de la transcripción exactamente así: [Hablante X]: [Texto transcrito]
                    3. Asegúrate de que la transcripción sea literal, completa y en español.
                    4. Si el audio no es claro, no contiene voz, o está en otro idioma, indícalo explícitamente.
                    
                    Procede con el análisis.
                    """
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{tipo_mime};base64,{audio_base64}"
                    }
                }
            ]
        )

        print("      TOOL-SYSTEM: -> Enviando audio y prompt a Gemini 1.5 para análisis...")
        respuesta = modelo_gemini_flash.invoke([mensaje_multimodal])
        transcripcion = str(respuesta.content)

        print("      TOOL-SYSTEM: -> ¡Análisis de audio completado! Transcripción recibida.")
        return transcripcion

    # --- BLOQUE DE MANEJO DE ERRORES CORREGIDO ---
    except Exception as e:
        # Imprimimos el error completo en el log para que nosotros (los desarrolladores) podamos verlo.
        print(f"      ERROR-CRITICO: Fallo en la transcripción con Gemini: {e}")
        # Pero retornamos un mensaje de error limpio y conciso para el sistema y el usuario.
        # Esto evita que el "montonero de texto" se guarde en la base de datos.
        return "Error: El modelo de IA no pudo procesar el archivo de audio. Posible causa: Límite de API excedido o archivo corrupto."

# --- FUNCIÓN DE INTERFAZ PÚBLICA (NO CAMBIA) ---
# Mantenemos esta función para no tener que cambiar el código de los agentes/nodos.
def procesar_audio(ruta_archivo: str) -> str:
    """
    Función principal de la herramienta de audio. Delega la transcripción
    al modelo multimodal Gemini.
    """
    return transcribir_audio_con_gemini(ruta_archivo)