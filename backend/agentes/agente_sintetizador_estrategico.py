# backend/agentes/agente_sintetizador_estrategico.py

from ..herramientas import herramientas_lenguaje

def generar_estrategia(texto_original: str, entidades: list[dict], informacion_recuperada: list[str]) -> dict:
    """
    Función de entrada para el Agente Sintetizador Estratégico.
    
    Toma todos los datos analizados y genera un borrador de recomendación.
    
    Args:
        texto_original (str): La transcripción o texto del documento.
        entidades (list[dict]): Las entidades extraídas.
        informacion_recuperada (list[str]): Los artículos legales recuperados.
        
    Returns:
        dict: Un diccionario con el borrador de la estrategia.
    """
    print("\n" + "*"*50)
    print("AGENT-SYSTEM: ¡AGENTE SINTETIZADOR ESTRATÉGICO ACTIVADO!")
    
    # 1. Construir un contexto completo para el LLM
    print("AGENT-SYSTEM: Decisión: Compilar todo el conocimiento en un único contexto.")
    contexto = f"Texto Original del Cliente: {texto_original}\n\n"
    contexto += f"Entidades Clave Identificadas: {entidades}\n\n"
    contexto += f"Artículos Legales Relevantes Recuperados de la Base de Conocimiento:\n"
    for articulo in informacion_recuperada:
        contexto += f"- {articulo}\n"
        
    # 2. Llamar a la herramienta de generación
    print("AGENT-SYSTEM: Decisión: Generar un borrador de estrategia legal.")
    borrador_estrategia = herramientas_lenguaje.generar_sintesis_con_llm(contexto)
    
    print(f"AGENT-SYSTEM: Borrador generado:\n{borrador_estrategia}")
    print("*"*50 + "\n")
    
    return {"borrador_estrategia": borrador_estrategia}