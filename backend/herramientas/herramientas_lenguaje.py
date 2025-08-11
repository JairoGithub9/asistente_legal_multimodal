# backend/herramientas/herramientas_lenguaje.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

from PIL import Image

import time


load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

modelo_gemini_pro = None
modelo_gemini_flash = None

if not api_key:
    print("TOOL-SETUP-ERROR: No se encontró la GOOGLE_API_KEY en el archivo .env")
else:
    genai.configure(api_key=api_key)
    print("TOOL-SETUP: API de Gemini configurada correctamente.")
    # 2. ¡OPTIMIZACIÓN! Creamos los modelos una sola vez para reutilizarlos.
    # Usaremos el 1.5 Pro para las tareas multimodales (video) y de alta calidad.
    modelo_gemini_pro = genai.GenerativeModel('gemini-1.5-pro-latest')
    # Usaremos el 1.5 Flash para tareas más rápidas y sencillas como la revisión.
    modelo_gemini_flash = genai.GenerativeModel('gemini-1.5-flash-latest') #gemini-2.5-pro-exp-03-25  gemini-1.5-flash-latest
    print("TOOL-SETUP: Modelos Gemini (Pro y Flash) inicializados.")


# 3. Cargar la base de conocimiento local
try:
    with open("datos/base_de_conocimiento_juridico/leyes_basicas.txt", "r", encoding="utf-8") as f:
        documentos_legales = f.read().split('---')
        documentos_legales = [doc.strip() for doc in documentos_legales if doc.strip()]
    print("TOOL-SETUP: Base de conocimiento cargada correctamente.")
except FileNotFoundError:
    documentos_legales = ["Error: No se encontró el archivo de la base de conocimiento."]
    print("TOOL-SETUP-ERROR: No se encontró el archivo de la base de conocimiento.")

# 4. Cargar el modelo para la búsqueda vectorial (RAG)
print("TOOL-SETUP: Cargando modelo de SentenceTransformer...")
modelo_sentencias = SentenceTransformer('all-MiniLM-L6-v2')
print("TOOL-SETUP: Modelo SentenceTransformer cargado.")

# 5. Crear el índice vectorial FAISS
print("TOOL-SETUP: Creando índice vectorial FAISS...")
embeddings_documentos = modelo_sentencias.encode(documentos_legales)
indice_faiss = faiss.IndexFlatL2(embeddings_documentos.shape[1])
indice_faiss.add(embeddings_documentos)
print("TOOL-SETUP: ¡Índice FAISS listo y cargado en memoria!")

# =================================================================================

# En backend/herramientas/herramientas_lenguaje.py

# En backend/herramientas/herramientas_lenguaje.py

def extraer_entidades_con_llm(texto: str) -> list[dict]:
    """
    Analiza un texto para extraer entidades clave usando el modelo Gemini.
    """
    print("      TOOL-SYSTEM: -> Herramienta REAL 'extraer_entidades_con_llm' activada.")
    
    if not api_key:
        print("      TOOL-SYSTEM: -> ERROR: La clave de API de Google no está configurada.")
        return [{"entidad": "Error de configuración de API", "tipo": "Error"}]


    
    
    prompt = f"""
    Eres un asistente legal experto en análisis de documentos en Colombia.
    Tu tarea es leer el siguiente texto y extraer las entidades más relevantes.
    Clasifica cada entidad en una de las siguientes categorías: 'Hecho Clave', 'Concepto Legal', 'Persona', 'Lugar', 'Fecha', 'Cuantía'.

    Devuelve el resultado ÚNICAMENTE en formato JSON, como una lista de objetos. No añadas texto introductorio ni explicaciones.

    Ejemplo de formato de salida:
    [
        {{"entidad": "accidente de tránsito", "tipo": "Hecho Clave"}},
        {{"entidad": "50 millones de pesos", "tipo": "Cuantía"}}
    ]

    Texto a analizar:
    ---
    {texto}
    ---
    """
    
    try:
        print("      TOOL-SYSTEM: -> Llamando a la API de Gemini para extraer entidades...")
        respuesta = modelo_gemini_flash.generate_content(prompt)
        
        respuesta_texto = respuesta.text
        if respuesta_texto.strip().startswith("```json"):
            respuesta_texto = respuesta_texto.strip()[7:-3]
        
        print("      TOOL-SYSTEM: -> Respuesta de Gemini recibida. Parseando JSON...")
        entidades = json.loads(respuesta_texto)
        print("      TOOL-SYSTEM: -> Extracción de entidades completada con éxito.")
        return entidades

    except Exception as e:
        print(f"      TOOL-SYSTEM: -> ERROR al llamar a la API de Gemini o parsear su respuesta: {e}")
        return [{"entidad": "Error en el procesamiento de IA", "tipo": "Error"}]


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

# En backend/herramientas/herramientas_lenguaje.py

def generar_sintesis_con_llm(contexto: str) -> str:
    """
    Toma un contexto completo y genera una síntesis o recomendación estratégica
    utilizando el modelo Gemini.
    """
    print("      TOOL-SYSTEM: -> Herramienta REAL 'generar_sintesis_con_llm' activada.")
    
    # 1. Seleccionamos el modelo
   
    
    # 2. Diseñamos un prompt específico para la tarea de síntesis
    prompt = f"""
    Eres un abogado senior y director de un consultorio jurídico en Colombia.
    Tu tarea es revisar el siguiente contexto, que incluye la narración de un cliente,
    entidades clave extraídas y artículos legales relevantes, y redactar un
    "Borrador de Estrategia Legal Preliminar".

    El borrador debe ser claro, estructurado y profesional. Usa Markdown para el formato.
    Debes incluir:
    1.  Un resumen muy breve del caso.
    2.  El fundamento legal principal, citando los artículos recuperados.
    3.  Una identificación clara de quién podría ser demandado.
    4.  Una consideración sobre la competencia del consultorio jurídico.
    5.  Un próximo paso concreto y recomendado.

    Contexto para analizar:
    ---
    {contexto}
    ---
    """

    try:
        # 3. Hacemos la llamada a la API de Gemini
        print("      TOOL-SYSTEM: -> Llamando a la API de Gemini para generar la síntesis...")
        respuesta = modelo_gemini_flash.generate_content(prompt)
        
        print("      TOOL-SYSTEM: -> Síntesis de Gemini recibida.")
        return respuesta.text

    except Exception as e:
        print(f"      TOOL-SYSTEM: -> ERROR al generar la síntesis con Gemini: {e}")
        return "Error: No se pudo generar la síntesis estratégica."
    

# En backend/herramientas/herramientas_lenguaje.py
# ... (las otras funciones no cambian) ...

def verificar_calidad_con_llm(borrador: str, contexto_original: str) -> dict:
    """
    Revisa un borrador estratégico para verificar su coherencia y fundamentación.
    """
    print("      TOOL-SYSTEM: -> Herramienta REAL 'verificar_calidad_con_llm' activada.")
    
    if not api_key:
        return {"verificado": False, "observaciones": "Error: La clave de API no está configurada."}

     # Usamos flash, es suficiente para una revisión
    
    prompt = f"""
    Eres un auditor legal extremadamente meticuloso y escéptico.
    Tu tarea es revisar el siguiente "Borrador de Estrategia" y verificar si es coherente y si se fundamenta lógicamente en el "Contexto Original" que se te proporciona.

    Realiza las siguientes comprobaciones:
    1.  ¿El resumen del caso en el borrador coincide con los hechos del texto original?
    2.  ¿Los fundamentos legales mencionados en el borrador realmente provienen de los artículos recuperados en el contexto?
    3.  ¿La recomendación final es una conclusión lógica de todo lo anterior?

    Devuelve tu veredicto ÚNICAMENTE en formato JSON con dos claves: "verificado" (un booleano true/false) y "observaciones" (una cadena de texto con tu justificación).

    Ejemplo de salida:
    {{"verificado": true, "observaciones": "El borrador es coherente, está bien fundamentado en los artículos recuperados y la recomendación es lógica."}}

    ---
    Borrador a Revisar:
    {borrador}
    ---
    Contexto Original para Verificar:
    {contexto_original}
    ---
    """
    
    try:
        print("      TOOL-SYSTEM: -> Llamando a Gemini para la verificación de calidad...")
        respuesta = modelo_gemini_flash.generate_content(prompt)
        
        respuesta_texto = respuesta.text
        if respuesta_texto.strip().startswith("```json"):
            respuesta_texto = respuesta_texto.strip()[7:-3]
        
        print("      TOOL-SYSTEM: -> Veredicto de calidad recibido.")
        veredicto = json.loads(respuesta_texto)
        return veredicto
    except Exception as e:
        print(f"      TOOL-SYSTEM: -> ERROR al verificar la calidad con Gemini: {e}")
        return {"verificado": False, "observaciones": f"Error técnico durante la verificación: {e}"}   





#-----------------------        



def describir_imagenes_con_gemini(rutas_imagenes: list[str], prompt_texto: str) -> list[str]:
    """
    Analiza una lista de imágenes usando Gemini-Flash para mayor velocidad y
    para respetar los límites de la API de la capa gratuita.
    """
    descripciones = []
    print(f"      TOOL-SYSTEM: -> Herramienta 'describir_imagenes_con_gemini' activada para {len(rutas_imagenes)} imágenes.")
    
    # --- ¡AQUÍ ESTÁ EL CAMBIO ESTRATÉGICO! ---
    # Usamos el modelo FLASH, que es más rápido y tiene una cuota más generosa.
    if not modelo_gemini_flash:
        print("      TOOL-SYSTEM-ERROR: El modelo Gemini Flash no está disponible.")
        return ["Error: El modelo Gemini Flash no está configurado."]

    for i, ruta_imagen in enumerate(rutas_imagenes):
        print(f"      TOOL-SYSTEM: -> Analizando imagen {i+1}/{len(rutas_imagenes)}: {ruta_imagen}")
        try:
            imagen = Image.open(ruta_imagen)
            contenido_request = [prompt_texto, imagen]
            
            # Nos aseguramos de llamar al modelo correcto
            respuesta = modelo_gemini_flash.generate_content(contenido_request)
            
            if respuesta.text:
                descripciones.append(respuesta.text)
            else:
                descripciones.append(f"[No se pudo generar descripción para la imagen {i+1}]")

        except Exception as e:
            error_msg = f"Error al procesar la imagen {ruta_imagen} con Gemini: {e}"
            print(f"      TOOL-SYSTEM-ERROR: {error_msg}")
            descripciones.append(f"[{error_msg}]")
        
        # Mantenemos la pausa por si acaso, es una buena práctica
        if i < len(rutas_imagenes) - 1:
            pausa = 20
            print(f"      TOOL-SYSTEM: -> Pausa de {pausa} segundos para respetar el límite de la API...")
            time.sleep(pausa)
            
    print("      TOOL-SYSTEM: -> Análisis de imágenes completado.")
    return descripciones