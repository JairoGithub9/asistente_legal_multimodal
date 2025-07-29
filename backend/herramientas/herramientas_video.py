# backend/herramientas/herramientas_video.py

import cv2
import os
from pathlib import Path
import traceback

# Constante para controlar la frecuencia de extracción de fotogramas.
# Extraeremos una imagen cada 5 segundos de video.
SEGUNDOS_ENTRE_FOTOGRAMAS = 5

def procesar_video_con_opencv_y_gemini(ruta_archivo: str, id_caso: str) -> dict:
    """
    Procesa un archivo de video para extraer fotogramas clave usando OpenCV.

    Esta es la implementación real. La función hace lo siguiente:
    1. Crea un directorio único para almacenar los fotogramas del video.
    2. Abre el archivo de video con OpenCV.
    3. Itera a través del video y guarda un fotograma a intervalos regulares.
    4. Retorna un resumen del trabajo realizado. Más adelante, estas imágenes se
       enviarán a un modelo de IA para su análisis.

    Args:
        ruta_archivo (str): La ruta completa al archivo de video.
        id_caso (str): El ID del caso, usado para crear la carpeta de fotogramas.

    Returns:
        dict: Un diccionario con 'texto_extraido' y 'error'.
    """
    resultado = {"texto_extraido": None, "error": None}
    print(f"      TOOL-SYSTEM: -> Herramienta REAL 'procesar_video' activada para {ruta_archivo}")

    # Inicializamos las variables fuera del bloque try
    captura_video = None
    rutas_fotogramas_guardados = []
    
    try:
        # 1. Creamos la ruta para guardar los fotogramas
        nombre_base_archivo = Path(ruta_archivo).stem
        ruta_guardado_fotogramas = Path("archivos_subidos") / id_caso / f"fotogramas_{nombre_base_archivo}"
        ruta_guardado_fotogramas.mkdir(parents=True, exist_ok=True)
        print(f"      TOOL-SYSTEM: -> Guardando fotogramas en: {ruta_guardado_fotogramas}")

        # 2. Abrimos el video con OpenCV
        captura_video = cv2.VideoCapture(ruta_archivo)
        if not captura_video.isOpened():
            raise IOError("No se pudo abrir el archivo de video.")

        # 3. Obtenemos los fotogramas por segundo (FPS) del video
        fps = captura_video.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30 # Usamos un valor por defecto si no se puede leer el FPS
        
        salto_entre_fotogramas = int(fps * SEGUNDOS_ENTRE_FOTOGRAMAS)
        contador_fotogramas = 0

        print(f"      TOOL-SYSTEM: -> Video con {fps:.2f} FPS. Extrayendo un fotograma cada {salto_entre_fotogramas} cuadros.")

        # 4. Leemos el video fotograma a fotograma
        while captura_video.isOpened():
            exito, fotograma = captura_video.read()
            if not exito:
                break # Se alcanzó el final del video

            # 5. Guardamos el fotograma si está en el intervalo deseado
            if contador_fotogramas % salto_entre_fotogramas == 0:
                segundo_actual = contador_fotogramas // fps
                nombre_fotograma = f"fotograma_segundo_{int(segundo_actual)}.jpg"
                ruta_completa_fotograma = str(ruta_guardado_fotogramas / nombre_fotograma)
                
                cv2.imwrite(ruta_completa_fotograma, fotograma)
                rutas_fotogramas_guardados.append(ruta_completa_fotograma)

            contador_fotogramas += 1
        
        # 6. Preparamos el resultado del procesamiento
        if rutas_fotogramas_guardados:
            texto_resultado = (
                f"Video procesado con éxito. Se extrajeron {len(rutas_fotogramas_guardados)} fotogramas clave "
                f"de un video de aproximadamente {int(contador_fotogramas / fps)} segundos. "
                f"Las imágenes se guardaron en la carpeta del caso para su posterior análisis."
            )
            resultado["texto_extraido"] = texto_resultado
            print(f"      TOOL-SYSTEM: -> ¡Éxito! Se extrajeron y guardaron {len(rutas_fotogramas_guardados)} fotogramas.")
        else:
            resultado["error"] = "No se pudo extraer ningún fotograma del video."

    except Exception as e:
        error_msg = f"Ocurrió un error inesperado al procesar el video con OpenCV: {e}"
        print(f"TOOL-SYSTEM-ERROR: {error_msg}")
        traceback.print_exc()
        resultado["error"] = error_msg
    finally:
        # Es crucial liberar el objeto de video para cerrar el archivo
        if captura_video:
            captura_video.release()
            
    return resultado