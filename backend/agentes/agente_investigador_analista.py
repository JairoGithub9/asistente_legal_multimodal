# backend/agentes/agente_investigador_analista.py

from ..herramientas import herramientas_lenguaje


# backend/agentes/agente_investigador_analista.py

from ..herramientas import herramientas_lenguaje

def analizar_texto_extraido(texto: str) -> dict:
    """
    Toma el texto procesado, extrae entidades y busca información relevante.
    """
    print("\n" + "#"*50)
    print("AGENT-SYSTEM: ¡AGENTE INVESTIGADOR Y ANALISTA ACTIVADO!")
    print(f"AGENT-SYSTEM: Analizando el siguiente texto: '{texto[:100]}...'")
    
    # 1. Extraer entidades
    print("AGENT-SYSTEM: Decisión: Extraer entidades clave del texto.")
    entidades = herramientas_lenguaje.extraer_entidades_con_llm(texto)
    
    # --- ¡NUEVO! PASO DE INVESTIGACIÓN (RAG) ---
    print("AGENT-SYSTEM: Decisión: Formular consulta para la base de conocimiento.")
    # Creamos una consulta simple a partir de las entidades encontradas
    consulta_rag = " ".join([e['entidad'] for e in entidades])
    
    print("AGENT-SYSTEM: Decisión: Buscar información relevante en la base de conocimiento.")
    informacion_relevante = herramientas_lenguaje.buscar_en_base_de_conocimiento(consulta_rag)
    
    print(f"AGENT-SYSTEM: Información recuperada: {informacion_relevante}")
    print("#"*50 + "\n")
    
    return {"entidades": entidades, "informacion_recuperada": informacion_relevante}