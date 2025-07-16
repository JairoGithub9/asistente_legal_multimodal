# backend/herramientas/herramientas_documentos.py

def procesar_pdf_con_nougat(ruta_archivo: str) -> str:
    """
    Procesa un archivo PDF para extraer su contenido textual estructurado.
    
    MODO SIMULACIÓN: Devuelve un texto de caso real para permitir
    que el resto de la cadena de agentes de IA funcione correctamente.
    
    Args:
        ruta_archivo (str): La ruta local del archivo PDF a procesar.

    Returns:
        str: El contenido del texto extraído del PDF.
    """
    print(f"      TOOL-SYSTEM: -> Herramienta 'procesar_pdf_con_nougat' activada para {ruta_archivo}")
    
    # Usamos el texto real de tu grabación para que Gemini tenga algo que analizar.
    texto_simulado = """
    Tuve un accidente de tránsito en el que sufrí lección permanente y deformación física en el rostro 
    con capacidad superior a 180 días y solo busco reclamación de perfisos materiales que se componen 
    de lucros en sete y daño emergente por valores 50 millones de pesos colombianos. 
    Los responsables de la accidente es una empresa de servicio público que cuenta con aseguradora. 
    En el 23 años trabajo en construcción con menos de un salario mínimo y no he podido volver a trabajar 
    como consecuencia del accidente, el accidente ocurrió en la salía de Cúcuta de Complona.
    """
    
    print("      TOOL-SYSTEM: -> Procesamiento de PDF (simulado con texto real) completado.")
    return texto_simulado.strip()