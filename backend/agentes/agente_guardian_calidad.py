# backend/agentes/agente_guardian_calidad.py

from ..herramientas import herramientas_lenguaje

def revisar_estrategia(borrador: str, contexto_completo: str) -> dict:
    """
    Activa el proceso de revisión de calidad sobre un borrador de estrategia.
    """
    print("\n" + "!"*50)
    print("AGENT-SYSTEM: ¡AGENTE GUARDIÁN DE CALIDAD ACTIVADO!")
    print(f"AGENT-SYSTEM: Revisando el borrador: '{borrador[:100]}...'")
    
    veredicto = herramientas_lenguaje.verificar_calidad_con_llm(
        borrador=borrador,
        contexto_original=contexto_completo
    )
    
    print(f"AGENT-SYSTEM: Veredicto final: {veredicto}")
    print("!"*50 + "\n")
    
    return veredicto