# backend/herramientas/herramientas_lenguaje.py

import faiss
import numpy as np
import os
import json
from dotenv import load_dotenv
from PIL import Image
import base64
import io
import time

# --- Módulos Principales de IA ---
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
# ------------------------------------

# =================================================================================
# SECCIÓN 1: CONFIGURACIÓN INICIAL DEL CEREBRO DE LA APLICACIÓN
# =================================================================================

# 1. Cargar la clave de API desde el archivo .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

modelo_gemini_pro = None
modelo_gemini_flash = None

if not api_key:
    print("TOOL-SETUP-ERROR: No se encontró la GOOGLE_API_KEY en el archivo .env")
else:
    # 2. Inicializamos los modelos de IA que usaremos en toda la aplicación.
    #    Hacemos esto una sola vez para ser más eficientes.
    try:
        modelo_gemini_pro = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", google_api_key=api_key)
        modelo_gemini_flash = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=api_key)
        print("TOOL-SETUP: Modelos Gemini (Pro y Flash) inicializados vía LangChain.")
    except Exception as e:
        print(f"TOOL-SETUP-ERROR: No se pudieron inicializar los modelos de Gemini. Error: {e}")

# 3. Cargar y preparar la base de conocimiento local para búsquedas (RAG).
try:
    with open("backend/datos/base_de_conocimiento_juridico/leyes_basicas.txt", "r", encoding="utf-8") as f:
        documentos_legales = f.read().split('---')
    print("TOOL-SETUP: Base de conocimiento cargada correctamente.")
    
    print("TOOL-SETUP: Cargando modelo de SentenceTransformer para RAG...")
    modelo_sentencias = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("TOOL-SETUP: Creando índice vectorial FAISS para búsqueda rápida...")
    embeddings_documentos = modelo_sentencias.encode(documentos_legales)
    indice_faiss = faiss.IndexFlatL2(embeddings_documentos.shape[1])
    indice_faiss.add(embeddings_documentos)
    print("TOOL-SETUP: ¡Índice FAISS para RAG listo y cargado en memoria!")

except Exception as e:
    print(f"TOOL-SETUP-ERROR: Fallo al inicializar el sistema RAG. Error: {e}")
    documentos_legales = []
    indice_faiss = None

# =================================================================================
# SECCIÓN 2: HERRAMIENTAS DE LENGUAJE (LLAMADAS A LA IA)
# =================================================================================

def extraer_entidades_con_llm(texto: str) -> list[dict]:
    """
    Analiza un texto para extraer entidades clave usando el modelo Gemini-Flash.
    Utiliza un prompt robusto y una lógica de parseo para asegurar una salida JSON limpia.
    """
    if not modelo_gemini_flash:
        return [{"entidad": "Error: Modelo Gemini no inicializado.", "tipo": "Error"}]

    prompt = f"""
    Eres un asistente legal experto en análisis de documentos en Colombia.
    Tu tarea es leer el siguiente texto y extraer las entidades más relevantes.
    Clasifica cada entidad en una de las siguientes categorías: 'Hecho Clave', 'Concepto Legal', 'Persona', 'Lugar', 'Fecha', 'Cuantía'.

    Sigue estas instrucciones al pie de la letra:
    1. Piensa en las entidades que vas a extraer.
    2. Formatea tu respuesta como una lista de objetos JSON.
    3. Envuelve tu respuesta final y ÚNICAMENTE la lista JSON dentro de las etiquetas <json> y </json>. No añadas texto introductorio, explicaciones ni la palabra "json" al principio.

    Texto a analizar:
    ---
    {texto}
    ---
    """
    
    try:
        print("      TOOL-SYSTEM: -> Llamando a Gemini-Flash para extraer entidades...")
        respuesta = modelo_gemini_flash.invoke(prompt)
        respuesta_texto = respuesta.content
        
        print("      TOOL-SYSTEM: -> Respuesta recibida. Limpiando y parseando JSON...")
        inicio = respuesta_texto.find('<json>') + len('<json>')
        fin = respuesta_texto.rfind('</json>')
        
        if inicio == -1 or fin == -1 or fin < inicio:
            raise json.JSONDecodeError("No se encontraron las etiquetas <json> en la respuesta.", respuesta_texto, 0)

        json_limpio = respuesta_texto[inicio:fin].strip()
        entidades = json.loads(json_limpio)
        return entidades

    except Exception as e:
        print(f"      TOOL-SYSTEM-ERROR: Al extraer entidades: {e}")
        return [{"entidad": "Error en el procesamiento de IA", "tipo": "Error"}]


def buscar_en_base_de_conocimiento(consulta: str, top_k: int = 2) -> list[str]:
    """
    Busca los documentos más relevantes para una consulta en nuestra base de conocimiento local.
    """
    if not indice_faiss:
        return ["Error: El sistema de búsqueda RAG no está inicializado."]
        
    embedding_consulta = modelo_sentencias.encode([consulta])
    _, indices = indice_faiss.search(embedding_consulta, top_k)
    return [documentos_legales[i] for i in indices[0]]


def generar_sintesis_con_llm(contexto: str) -> str:
    """
    Toma un contexto completo y genera una síntesis o recomendación estratégica.
    """
    if not modelo_gemini_flash:
        return "Error: Modelo Gemini no inicializado."

    prompt = f"""
    Eres un abogado senior y director de un consultorio jurídico en Colombia.
    Tu tarea es revisar el siguiente contexto y redactar un "Borrador de Estrategia Legal Preliminar".
    El borrador debe ser claro, estructurado y profesional, usando Markdown.
    Debes incluir:
    1. Un resumen breve del caso.
    2. El fundamento legal principal, citando los artículos recuperados.
    3. Identificación de posibles demandados.
    4. Consideración sobre la competencia del consultorio.
    5. Un próximo paso concreto y recomendado.

    Contexto para analizar:
    ---
    {contexto}
    ---
    """
    try:
        print("      TOOL-SYSTEM: -> Llamando a Gemini-Flash para generar la síntesis...")
        respuesta = modelo_gemini_flash.invoke(prompt)
        return respuesta.content
    except Exception as e:
        print(f"      TOOL-SYSTEM-ERROR: Al generar la síntesis: {e}")
        return f"Error: No se pudo generar la síntesis estratégica."


def verificar_calidad_con_llm(borrador: str, contexto_original: str) -> dict:
    """
    Revisa un borrador estratégico para verificar su coherencia y fundamentación.
    """
    if not modelo_gemini_flash:
        return {"verificado": False, "observaciones": "Error: Modelo Gemini no inicializado."}

    prompt = f"""
    Eres un auditor legal meticuloso. Revisa el "Borrador de Estrategia" y verifica si es coherente
    y se fundamenta en el "Contexto Original".

    Comprueba:
    1. ¿El resumen coincide con los hechos originales?
    2. ¿Los fundamentos legales mencionados provienen de los artículos del contexto?
    3. ¿La recomendación final es una conclusión lógica?

    Devuelve tu veredicto ÚNICAMENTE en formato JSON, envuelto en etiquetas <json> y </json>,
    con dos claves: "verificado" (booleano) y "observaciones" (string).

    ---
    Borrador a Revisar:
    {borrador}
    ---
    Contexto Original para Verificar:
    {contexto_original}
    ---
    """
    try:
        print("      TOOL-SYSTEM: -> Llamando a Gemini-Flash para la verificación de calidad...")
        respuesta = modelo_gemini_flash.invoke(prompt)
        respuesta_texto = respuesta.content

        inicio = respuesta_texto.find('<json>') + len('<json>')
        fin = respuesta_texto.rfind('</json>')

        if inicio == -1 or fin == -1 or fin < inicio:
            raise json.JSONDecodeError("No se encontraron las etiquetas <json> en la respuesta.", respuesta_texto, 0)
        
        json_limpio = respuesta_texto[inicio:fin].strip()
        veredicto = json.loads(json_limpio)
        return veredicto
    except Exception as e:
        print(f"      TOOL-SYSTEM-ERROR: Al verificar la calidad: {e}")
        return {"verificado": False, "observaciones": f"Error técnico durante la verificación."}


def describir_imagenes_con_gemini(rutas_imagenes: list[str], prompt_texto: str) -> list[str]:
    """
    Analiza una lista de imágenes usando Gemini-Flash.

    VERSIÓN ROBUSTA:
    - Ahora convierte las imágenes con transparencia (modo RGBA, como los PNG)
      a modo RGB antes de procesarlas, evitando errores.
    - Mantiene las pausas para respetar los límites de la API.
    """
    descripciones = []
    if not modelo_gemini_flash:
        return ["Error: Modelo Gemini no inicializado." for _ in rutas_imagenes]

    for i, ruta_imagen in enumerate(rutas_imagenes):
        print(f"      TOOL-SYSTEM: -> Analizando imagen {i+1}/{len(rutas_imagenes)}...")
        try:
            imagen = Image.open(ruta_imagen)

            # --- ¡AQUÍ ESTÁ LA CORRECCIÓN PARA PNGs! ---
            # Si la imagen tiene transparencia (modo RGBA), la convertimos a RGB.
            if imagen.mode == 'RGBA':
                print("      TOOL-SYSTEM: -> Detectada imagen con transparencia (RGBA). Convirtiendo a RGB...")
                imagen = imagen.convert('RGB')
            # ----------------------------------------------

            buffered = io.BytesIO()
            imagen.save(buffered, format="JPEG") # Ahora esto siempre funcionará
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            mensaje = HumanMessage(
                content=[
                    {"type": "text", "text": prompt_texto},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}},
                ]
            )
            
            respuesta = modelo_gemini_flash.invoke([mensaje])
            descripciones.append(respuesta.content)

        except Exception as e:
            error_msg = f"Error al procesar la imagen {ruta_imagen}: {e}"
            print(f"      TOOL-SYSTEM-ERROR: {error_msg}")
            descripciones.append(f"[{error_msg}]")
        
        if i < len(rutas_imagenes) - 1:
            pausa = 20
            print(f"      TOOL-SYSTEM: -> Pausa de {pausa} segundos para respetar el límite de la API...")
            time.sleep(pausa)
            
    return descripciones