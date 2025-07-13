# backend/herramientas/herramientas_lenguaje.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# =================================================================================
# ¡CONFIGURACIÓN INICIAL! Esto se ejecutaría una sola vez o al iniciar el servidor.
# Por simplicidad, lo ponemos aquí por ahora.
# =================================================================================

# 1. Cargar los documentos de nuestra base de conocimiento
try:
    with open("datos/base_de_conocimiento_juridico/leyes_basicas.txt", "r", encoding="utf-8") as f:
        documentos_legales = f.read().split('---')
        documentos_legales = [doc.strip() for doc in documentos_legales if doc.strip()]
    print("TOOL-SETUP: Base de conocimiento cargada correctamente.")
except FileNotFoundError:
    documentos_legales = ["Error: No se encontró el archivo de la base de conocimiento."]
    print("TOOL-SETUP: ERROR! No se encontró el archivo de la base de conocimiento.")


# 2. Cargar el modelo para convertir texto a vectores
print("TOOL-SETUP: Cargando modelo de SentenceTransformer...")
modelo_sentencias = SentenceTransformer('all-MiniLM-L6-v2')
print("TOOL-SETUP: Modelo cargado.")

# 3. Crear el índice vectorial (la "base de datos" de búsqueda)
print("TOOL-SETUP: Creando índice vectorial FAISS...")
embeddings_documentos = modelo_sentencias.encode(documentos_legales)
indice_faiss = faiss.IndexFlatL2(embeddings_documentos.shape[1])
indice_faiss.add(embeddings_documentos)
print("TOOL-SETUP: ¡Índice FAISS listo y cargado en memoria!")

# =================================================================================

def extraer_entidades_con_llm(texto: str) -> list[dict]:
    """
    Analiza un texto para extraer entidades clave (simulado).
    """
    print("      TOOL-SYSTEM: -> Herramienta 'extraer_entidades_con_llm' activada.")
    entidades_simuladas = [
        {"entidad": "accidente de tránsito", "tipo": "Concepto Legal"},
        {"entidad": "lesión permanente", "tipo": "Hecho Clave"},
        {"entidad": "50 millones de pesos", "tipo": "Cuantía"},
        {"entidad": "empresa de servicio público", "tipo": "Persona Jurídica"},
    ]
    print("      TOOL-SYSTEM: -> Extracción de entidades completada.")
    return entidades_simuladas

def buscar_en_base_de_conocimiento(consulta: str, top_k: int = 2) -> list[str]:
    """
    Busca los documentos más relevantes para una consulta en nuestra base de conocimiento.
    """
    print(f"      TOOL-SYSTEM: -> Herramienta 'buscar_en_base_de_conocimiento' activada con la consulta: '{consulta}'")
    
    # Convertir la consulta en un vector
    embedding_consulta = modelo_sentencias.encode([consulta])
    
    # Buscar en FAISS los 'top_k' resultados más cercanos
    distancias, indices = indice_faiss.search(embedding_consulta, top_k)
    
    # Obtener los textos de los documentos correspondientes
    resultados = [documentos_legales[i] for i in indices[0]]
    
    print(f"      TOOL-SYSTEM: -> Búsqueda completada. {len(resultados)} resultados encontrados.")
    return resultados


# En backend/herramientas/herramientas_lenguaje.py
# ... (las otras funciones y la configuración inicial no cambian) ...

def generar_sintesis_con_llm(contexto: str) -> str:
    """
    Toma un contexto completo y genera una síntesis o recomendación estratégica.
    
    En el futuro, esta función enviará el contexto a un LLM de generación (Gemini).
    Por ahora, simula una respuesta basada en el contexto.
    
    Args:
        contexto (str): Un texto largo que contiene la transcripción, las
                        entidades y la información legal recuperada.

    Returns:
        str: Un borrador de la síntesis estratégica.
    """
    print("      TOOL-SYSTEM: -> Herramienta 'generar_sintesis_con_llm' activada.")
    
    # Lógica futura para construir un prompt y llamar a Gemini.
    
    # Simulamos una respuesta basada en palabras clave del contexto
    borrador_estrategico = "### Borrador de Estrategia Legal Preliminar\n\n"
    borrador_estrategico += "**1. Resumen del Caso:** El caso trata de un accidente de tránsito con lesiones personales graves.\n"
    
    if "responsabilidad civil" in contexto.lower():
        borrador_estrategico += "**2. Fundamento Legal:** La reclamación se basa en la Responsabilidad Civil Extracontractual (Artículo 2 recuperado).\n"
    if "empresa de servicio público" in contexto.lower():
        borrador_estrategico += "**3. Sujeto Pasivo (Demandado):** Se puede demandar tanto al conductor como a la empresa de transporte de manera solidaria (Artículo 3 recuperado).\n"
    if "cuantía" in contexto.lower() and "consultorios jurídicos" in contexto.lower():
         borrador_estrategico += "**4. Competencia:** Dado que la cuantía es de 50 millones, se debe verificar si supera el tope de los 40 SMLMV para la competencia de consultorios jurídicos (Artículo 1 recuperado).\n"
    
    borrador_estrategico += "**5. Próximo Paso Recomendado:** Preparar una reclamación formal a la aseguradora del vehículo de servicio público."
    
    print("      TOOL-SYSTEM: -> Generación de síntesis completada.")
    return borrador_estrategico