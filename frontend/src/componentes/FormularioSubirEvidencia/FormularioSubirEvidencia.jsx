// frontend/src/componentes/FormularioSubirEvidencia/FormularioSubirEvidencia.jsx

import React, { useState } from 'react';
import './FormularioSubirEvidencia.css';

/**
 * Componente de formulario con una única responsabilidad:
 * - Permitir al usuario seleccionar un archivo.
 * - Avisar a su componente padre cuando el usuario quiere subir el archivo.
 * - Gestionar su propio estado de "subiendo" para dar feedback al usuario.
 */
const FormularioSubirEvidencia = ({ onArchivoSeleccionado, estaProcesando }) => {
  // Estado para guardar el archivo que el usuario elige.
  const [archivo, setArchivo] = useState(null);

  /**
   * Se ejecuta cuando el usuario elige un archivo del explorador.
   */
  const manejarSeleccionArchivo = (evento) => {
    setArchivo(evento.target.files[0]);
  };

  /**
   * Se ejecuta cuando el usuario hace clic en el botón "Subir Archivo".
   * Ahora es mucho más simple.
   */
  const manejarEnvio = async (evento) => {
    evento.preventDefault();
    if (!archivo) {
      alert("Por favor, selecciona un archivo primero.");
      return;
    }

    // ¡AVISAMOS AL PADRE!
    // Llamamos a la función que nos pasó el componente padre (`VistaDetalleCaso`),
    // y le entregamos el archivo que el usuario seleccionó.
    // El padre se encargará de la lógica de subida y de poner `estaProcesando` en true.
    await onArchivoSeleccionado(archivo);
    
    // Limpiamos el formulario para la siguiente subida.
    setArchivo(null);
    evento.target.reset();
  };

  return (
    <form onSubmit={manejarEnvio} className="upload-form">
      <h4>Añadir Nueva Evidencia</h4>
      <input type="file" onChange={manejarSeleccionArchivo} />
      {/* El botón ahora se deshabilita con la prop `estaProcesando` que le pasa el padre */}
      <button type="submit" disabled={!archivo || estaProcesando}>
        {estaProcesando ? 'Procesando...' : 'Subir Archivo'}
      </button>
    </form>
  );
};

export default FormularioSubirEvidencia;