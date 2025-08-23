// frontend/src/servicios/api.js

const URL_BASE = 'http://127.0.0.1:8000';

export const crearNuevoCaso = async (titulo, resumen) => {
  const datosFormulario = {
    titulo: titulo,
    resumen: resumen,
  };

  console.log("Servicio API: Enviando datos para crear caso:", datosFormulario);

  try {
    const respuesta = await fetch(`${URL_BASE}/casos`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(datosFormulario),
    });

    if (!respuesta.ok) {
      throw new Error(`Error del servidor: ${respuesta.status}`);
    }

    const casoCreado = await respuesta.json();
    console.log("Servicio API: Caso creado con éxito:", casoCreado);
    return casoCreado;

  } catch (error) {
    console.error("Servicio API: Error al crear el caso:", error);
    // "Relanzamos" el error para que el componente que llamó sepa que algo salió mal.
    throw error;
  }
};


export const obtenerTodosLosCasos = async () => {
  console.log("Servicio API: Pidiendo la lista de todos los casos...");
  try {
    const respuesta = await fetch(`${URL_BASE}/casos`);
    if (!respuesta.ok) {
      throw new Error(`Error del servidor: ${respuesta.status}`);
    }
    const casos = await respuesta.json();
    console.log("Servicio API: Lista de casos recibida.", casos);
    return casos;
  } catch (error) {
    console.error("Servicio API: Error al obtener los casos:", error);
    throw error;
  }
};

// En el futuro, aquí añadiremos más funciones como:
// export const subirEvidencia = async (idCaso, archivo) => { ... }
// export const obtenerCaso = async (idCaso) => { ... }

export const subirEvidencia = async (idCaso, archivo) => {
  // Usamos FormData para enviar archivos
  const formData = new FormData();
  formData.append("archivo", archivo);

  console.log(`Servicio API: Subiendo archivo '${archivo.name}' para el caso ${idCaso}`);

  try {
    const respuesta = await fetch(`${URL_BASE}/casos/${idCaso}/evidencia`, {
      method: 'POST',
      // ¡Importante! No establecemos 'Content-Type'. 
      // El navegador lo hará automáticamente con el 'boundary' correcto para FormData.
      body: formData,
    });

    if (!respuesta.ok) {
      throw new Error(`Error del servidor: ${respuesta.status}`);
    }

    const casoActualizado = await respuesta.json();
    console.log("Servicio API: Evidencia subida. Caso actualizado:", casoActualizado);
    return casoActualizado;
  } catch (error) {
    console.error("Servicio API: Error al subir la evidencia:", error);
    throw error;
  }
};


/**
 * Consulta el estado de una evidencia específica.
 * @param {string} idEvidencia - El UUID de la evidencia a consultar.
 * @returns {Promise<object>} Una promesa que resuelve a un objeto con el estado.
 *                            Ej: { estado_procesamiento: 'completado' }
 */
export const obtenerEstadoEvidencia = async (idEvidencia) => {
  try {
    // Usamos fetch para hacer la petición GET al nuevo endpoint
    const respuesta = await fetch(`${URL_BASE}/evidencias/${idEvidencia}/estado`);
    
    if (!respuesta.ok) {
      throw new Error(`Error del servidor: ${respuesta.status}`);
    }
    
    const datosEstado = await respuesta.json();
    return datosEstado;

  } catch (error) {
    console.error(`Error al obtener el estado de la evidencia ${idEvidencia}:`, error);
    // Devolvemos un estado de error para que el polling pueda detenerse si falla la llamada
    return { estado_procesamiento: 'error_en_sondeo' };
  }
};