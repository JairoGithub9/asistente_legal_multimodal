// frontend/src/componentes/FormularioSubirEvidencia/FormularioSubirEvidencia.jsx
import { useState } from 'react';
import { subirEvidencia } from '../../servicios/api';
import './FormularioSubirEvidencia.css';

const FormularioSubirEvidencia = ({ idCaso, onEvidenciaSubida }) => {
  const [archivo, setArchivo] = useState(null);
  const [estaSubiendo, setEstaSubiendo] = useState(false);

  const manejarSeleccionArchivo = (evento) => {
    setArchivo(evento.target.files[0]);
  };

  const manejarEnvio = async (evento) => {
    evento.preventDefault();
    if (!archivo) {
      alert("Por favor, selecciona un archivo primero.");
      return;
    }

    setEstaSubiendo(true);
    try {
      const casoActualizado = await subirEvidencia(idCaso, archivo);
      alert(`¡Evidencia '${archivo.name}' subida con éxito!`);
      onEvidenciaSubida(casoActualizado); // Avisamos al componente padre
    } catch (error) {
      alert(error.message,"Hubo un error al subir la evidencia.");
    } finally {
      setEstaSubiendo(false);
      setArchivo(null);
      evento.target.reset(); // Limpia el input de archivo
    }
  };

  return (
    <form onSubmit={manejarEnvio} className="upload-form">
      <h4>Añadir Nueva Evidencia</h4>
      <input type="file" onChange={manejarSeleccionArchivo} />
      <button type="submit" disabled={!archivo || estaSubiendo}>
        {estaSubiendo ? 'Subiendo...' : 'Subir Archivo'}
      </button>
    </form>
  );
};

export default FormularioSubirEvidencia;