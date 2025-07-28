# backend/herramientas/herramientas_documentos.py

from pathlib import Path
from nougat import NougatModel
from nougat.utils.checkpoint import get_checkpoint
import fitz  # PyMuPDF
from PIL import Image

# =================================================================================
# ¡CONFIGURACIÓN INICIAL DE NOUGAT!
# =================================================================================
try:
    print("TOOL-SETUP: Configurando el modelo Nougat...")
    checkpoint_path = get_checkpoint() 
    modelo_nougat = NougatModel.from_pretrained(checkpoint_path)
    print("TOOL-SETUP: ¡Modelo Nougat cargado y listo para procesar documentos!")
except Exception as e:
    modelo_nougat = None
    print(f"TOOL-SETUP-ERROR: No se pudo cargar o configurar el modelo Nougat. Error: {e}")
# =================================================================================


def procesar_pdf_con_nougat(ruta_archivo: str) -> dict:
    """Procesa un archivo PDF utilizando el modelo Nougat página por página.

    Esta es la implementación final y robusta. Primero, abre el PDF con PyMuPDF.
    Luego, itera sobre cada página, la convierte en una imagen de alta calidad,
    y pasa esa imagen individualmente al método 'inference' de Nougat.
    Finalmente, une los textos de todas las páginas.

    Args:
        ruta_archivo (str): La ruta local completa del archivo PDF a procesar.

    Returns:
        dict: Un diccionario con 'texto_extraido' (str) y 'error' (str o None).
    """
    resultado = {"texto_extraido": None, "error": None}
    if not modelo_nougat:
        resultado["error"] = "Modelo Nougat no disponible."
        print(f"TOOL-SYSTEM-ERROR: {resultado['error']}")
        return resultado

    print(f"      TOOL-SYSTEM: -> Herramienta REAL 'procesar_pdf_con_nougat' activada para {ruta_archivo}")
    
    documento_pdf = None # Inicializamos fuera del try para poder cerrarlo en finally
    try:
        documento_pdf = fitz.open(ruta_archivo)
        textos_de_paginas = []
        print(f"      TOOL-SYSTEM: -> Procesando {len(documento_pdf)} página(s) del PDF...")

        # 1. Iteramos sobre cada página del documento
        for numero_pagina, pagina in enumerate(documento_pdf):
            print(f"      TOOL-SYSTEM: -> Procesando página {numero_pagina + 1}...")
            
            # 2. Convertimos la página en una imagen de alta calidad
            pix = pagina.get_pixmap(dpi=96)
            imagen_pagina = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # 3. ¡LA LLAMADA CORRECTA! Le pasamos la imagen al método 'inference'.
            salida_modelo = modelo_nougat.inference(image=imagen_pagina)
            
            # 4. Extraemos el texto de la predicción de la página
            texto_pagina = salida_modelo['predictions'][0]
            textos_de_paginas.append(texto_pagina)

        # 5. Unimos el texto de todas las páginas
        resultado["texto_extraido"] = "\n\n".join(textos_de_paginas)
        print("      TOOL-SYSTEM: -> Procesamiento de PDF con Nougat completado.")

    except Exception as e:
        error_msg = f"Ocurrió un error inesperado al procesar el PDF con Nougat: {e}"
        print(f"TOOL-SYSTEM-ERROR: {error_msg}")
        resultado["error"] = error_msg
    finally:
        # Es una buena práctica cerrar siempre el archivo PDF
        if documento_pdf:
            documento_pdf.close()
            
    return resultado

def procesar_documento_simulado(ruta_archivo: str) -> dict:
    """Simula el procesamiento de un archivo para pruebas de respaldo."""
    print("      TOOL-SYSTEM: -> Herramienta 'procesar_documento_simulado' activada.")
    return {"texto_extraido": "Texto simulado.", "error": None}