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

// En el futuro, aquí añadiremos más funciones como:
// export const subirEvidencia = async (idCaso, archivo) => { ... }
// export const obtenerCaso = async (idCaso) => { ... }