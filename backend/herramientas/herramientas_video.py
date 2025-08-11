# backend/herramientas/herramientas_video.py

import cv2
from pathlib import Path
import traceback

# Importamos las herramientas de lenguaje para poder llamar a la IA
from . import herramientas_lenguaje

# --- Constantes de Configuración ---

# Extraeremos una imagen cada 5 segundos de video.
SEGUNDOS_ENTRE_FOTOGRAMAS = 5

# Este es el prompt que le daremos a la IA para que analice cada fotograma.
PROMPT_ANALISIS_IMAGEN = """
Eres un investigador forense y asistente legal. Tu tarea es describir la siguiente imagen
de manera objetiva, detallada y precisa para un informe de un caso.

En tu descripción, céntrate en los siguientes puntos si están presentes:
- **Personas:** Describe su apariencia, ropa y acciones. No adivines su estado emocional.
- **Vehículos:** Describe el tipo, color y, si es legible, la matrícula.
- **Objetos:** Menciona cualquier objeto relevante en la escena.
- **Entorno:** Describe la ubicación (calle, interior, etc.) y las condiciones (día, noche, etc.).
- **Texto:** Transcribe cualquier texto visible en la imagen (señales, carteles, etc.).

Sé conciso y cíñete a los hechos visuales.
"""

def procesar_video_con_opencv_y_gemini(ruta_archivo: str, id_caso: str) -> dict:
    """
    Orquesta el procesamiento completo de un video: extrae fotogramas con OpenCV
    y luego los analiza con un modelo de IA multimodal (Gemini) para describir su contenido.

    Args:
        ruta_archivo (str): La ruta completa al archivo de video.
        id_caso (str): El ID del caso, para organizar los archivos.

    Returns:
        dict: Un diccionario con 'texto_extraido' (un informe completo de lo que
              se ve en el video) y 'error'.
    """
    resultado = {"texto_extraido": None, "error": None}
    print(f"      TOOL-SYSTEM: -> Herramienta REAL 'procesar_video' activada para {ruta_archivo}")

    captura_video = None
    rutas_fotogramas_guardados = []
    
    try:
        # --- FASE 1: Extracción de Fotogramas con OpenCV ---
        
        # (Esta parte es la misma que ya teníamos y funcionaba)
        nombre_base_archivo = Path(ruta_archivo).stem
        ruta_guardado_fotogramas = Path("archivos_subidos") / id_caso / f"fotogramas_{nombre_base_archivo}"
        ruta_guardado_fotogramas.mkdir(parents=True, exist_ok=True)
        print(f"      TOOL-SYSTEM: -> [Fase 1/2] Extrayendo fotogramas a: {ruta_guardado_fotogramas}")

        captura_video = cv2.VideoCapture(ruta_archivo)
        if not captura_video.isOpened():
            raise IOError("No se pudo abrir el archivo de video.")

        fps = captura_video.get(cv2.CAP_PROP_FPS) or 30
        salto_entre_fotogramas = int(fps * SEGUNDOS_ENTRE_FOTOGRAMAS)
        contador_fotogramas = 0

        while captura_video.isOpened():
            exito, fotograma = captura_video.read()
            if not exito: break

            if contador_fotogramas % salto_entre_fotogramas == 0:
                segundo_actual = int(contador_fotogramas / fps)
                nombre_fotograma = f"fotograma_segundo_{segundo_actual}.jpg"
                ruta_completa_fotograma = str(ruta_guardado_fotogramas / nombre_fotograma)
                cv2.imwrite(ruta_completa_fotograma, fotograma)
                rutas_fotogramas_guardados.append(ruta_completa_fotograma)

            contador_fotogramas += 1
        
        print(f"      TOOL-SYSTEM: -> [Fase 1/2] Extracción completada. Se guardaron {len(rutas_fotogramas_guardados)} fotogramas.")

        if not rutas_fotogramas_guardados:
            resultado["error"] = "No se pudo extraer ningún fotograma del video."
            return resultado

        # --- FASE 2: Análisis de Fotogramas con IA (Gemini) ---
        print(f"      TOOL-SYSTEM: -> [Fase 2/2] Enviando fotogramas a la IA para su análisis...")
        
        descripciones_ia = herramientas_lenguaje.describir_imagenes_con_gemini(
            rutas_imagenes=rutas_fotogramas_guardados,
            prompt_texto=PROMPT_ANALISIS_IMAGEN
        )

        # --- FASE 3: Consolidación del Informe ---
        print("      TOOL-SYSTEM: -> [Fase 3/3] Consolidando el informe final del video.")
        informe_final = [
            "INFORME DE ANÁLISIS DE EVIDENCIA EN VIDEO\n"
            "========================================\n",
            f"El siguiente texto es una transcripción generada por IA del contenido visual de {len(descripciones_ia)} fotogramas clave extraídos del video '{Path(ruta_archivo).name}'.\n"
        ]

        for i, descripcion in enumerate(descripciones_ia):
            segundo_aprox = i * SEGUNDOS_ENTRE_FOTOGRAMAS
            informe_final.append(f"\n--- Fotograma {i+1} (aproximadamente en el segundo {segundo_aprox}) ---\n")
            informe_final.append(descripcion)
        
        resultado["texto_extraido"] = "\n".join(informe_final)
        print("      TOOL-SYSTEM: -> ¡Análisis completo! Informe de video generado.")

    except Exception as e:
        error_msg = f"Ocurrió un error inesperado al procesar el video: {e}"
        print(f"TOOL-SYSTEM-ERROR: {error_msg}")
        traceback.print_exc()
        resultado["error"] = error_msg
    finally:
        if captura_video:
            captura_video.release()
            
    return resultado