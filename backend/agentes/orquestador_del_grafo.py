# backend/agentes/orquestador_del_grafo.py

from langgraph.graph import StateGraph
from .estado_del_grafo import EstadoDelGrafo
from .nodos_del_grafo import (
    nodo_procesador_evidencia,
    nodo_investigador_analista,
    nodo_sintetizador_estrategico,
    nodo_guardian_calidad
)

# =================================================================================
# PASO 1: DEFINIR EL GRAFO Y LOS NODOS (Sin cambios)
# =================================================================================
flujo_de_trabajo = StateGraph(EstadoDelGrafo)
print("SETUP-LANGGRAPH: Creando el grafo de agentes...")

flujo_de_trabajo.add_node("procesador_evidencia", nodo_procesador_evidencia)
flujo_de_trabajo.add_node("investigador_analista", nodo_investigador_analista)
flujo_de_trabajo.add_node("sintetizador_estrategico", nodo_sintetizador_estrategico)
flujo_de_trabajo.add_node("guardian_de_calidad", nodo_guardian_calidad)

print("SETUP-LANGGRAPH: Nodos añadidos al grafo.")

# =================================================================================
# PASO 2: DEFINIR LA LÓGICA DE DECISIÓN (EL SUPERVISOR)
# =================================================================================
def supervisor_de_calidad(estado: EstadoDelGrafo) -> str:
    """
    Actúa como un supervisor inteligente para decidir el siguiente paso.
    """
    print("\n--- Entrando en el Supervisor de Calidad ---")
    
    # --- ¡LA CORRECCIÓN! ---
    # Cambiamos de la sintaxis de diccionario (estado.get("clave")) a la
    # sintaxis de objeto (estado.atributo) para acceder a los datos.
    if estado.entidades_extraidas is None or estado.borrador_estrategia is None:
        print("    Decisión: Faltan datos críticos de nodos anteriores. Finalizando el ciclo.")
        return "__end__"
    # -----------------------------------------------
    
    # Lógica del límite de intentos (esta ya era correcta)
    MAXIMOS_INTENTOS = 2
    intentos = estado.intentos_correccion
    if intentos >= MAXIMOS_INTENTOS:
        print(f"    Decisión: Se ha alcanzado el límite de {MAXIMOS_INTENTOS} intentos. Finalizando.")
        return "__end__"

    # Lógica del veredicto (esta ya era correcta)
    veredicto = estado.verificacion_calidad
    if veredicto and veredicto.get("verificado"): # Usamos .get() aquí porque 'veredicto' SÍ es un diccionario
        print("    Decisión: El borrador cumple con los estándares. Finalizando.")
        return "__end__"
    else:
        print(f"    Decisión: El borrador NO cumple (Intento {intentos}). Devolviendo al Sintetizador.")
        return "sintetizador_estrategico"
# =================================================================================
# PASO 3: CONECTAR LOS NODOS PARA CREAR EL DIAGRAMA DE FLUJO
# =================================================================================
print("SETUP-LANGGRAPH: Definiendo las conexiones del grafo...")

# 3.1. Punto de entrada
flujo_de_trabajo.set_entry_point("procesador_evidencia")

# 3.2. Conexiones lineales
flujo_de_trabajo.add_edge("procesador_evidencia", "investigador_analista")
flujo_de_trabajo.add_edge("investigador_analista", "sintetizador_estrategico")
flujo_de_trabajo.add_edge("sintetizador_estrategico", "guardian_de_calidad")

# 3.3. ¡LA NUEVA CONEXIÓN INTELIGENTE (BIFURCACIÓN)!
flujo_de_trabajo.add_conditional_edges(
    # Nodo de origen: Desde dónde se toma la decisión.
    "guardian_de_calidad",
    # Función supervisora: La función que decide el camino.
    supervisor_de_calidad,
    # Mapa de decisiones: Un diccionario que traduce la salida del supervisor
    # a un destino.
    {
        "sintetizador_estrategico": "sintetizador_estrategico", # Si devuelve "sintetizador...", vamos a ese nodo.
        "__end__": "__end__"  # Si devuelve "__end__", terminamos.
    }
)

print("SETUP-LANGGRAPH: ¡Conexiones del grafo, incluyendo el bucle, definidas!")

# =================================================================================
# PASO 4: COMPILAR EL GRAFO (Sin cambios)
# =================================================================================
grafo_compilado = flujo_de_trabajo.compile()
print("SETUP-LANGGRAPH: ¡Grafo de agentes compilado y listo para usar!")

try:
    imagen_en_bytes = grafo_compilado.get_graph().draw_png()
    with open("grafo_agentes_con_bucle.png", "wb") as f:
        f.write(imagen_en_bytes)
    print("SETUP-LANGGRAPH: Se ha guardado una imagen del grafo en 'grafo_agentes_con_bucle.png'.")
except Exception as e:
    print(f"SETUP-LANGGRAPH-WARN: No se pudo generar la imagen del grafo. Causa: {e}")