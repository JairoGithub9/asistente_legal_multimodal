// frontend/src/componentes/FormularioCrearCaso/FormularioCrearCaso.jsx

import { useState } from 'react';
// Importamos la función de nuestro servicio de API
import { crearNuevoCaso } from '../../servicios/api';
// Importamos los estilos específicos para este componente
import './FormularioCrearCaso.css';

const FormularioCrearCaso = () => {
  const [titulo, setTitulo] = useState('');
  const [resumen, setResumen] = useState('');

  const manejarEnvio = async (evento) => {
    evento.preventDefault();
    try {
      const casoCreado = await crearNuevoCaso(titulo, resumen);
      alert(`¡Caso creado con éxito! ID: ${casoCreado.id_caso}`);
      setTitulo('');
      setResumen('');
    } catch (error) {
      alert(error.message,"Hubo un error al crear el caso. Revisa la consola.");
    }
  };

  return (
    <form onSubmit={manejarEnvio} className="caso-form">
      <h2>Crear Nuevo Caso</h2>
      <div className="form-group">
        <label htmlFor="titulo">Título del Caso</label>
        <input
          type="text"
          id="titulo"
          value={titulo}
          onChange={(e) => setTitulo(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="resumen">Resumen Preliminar</label>
        <textarea
          id="resumen"
          value={resumen}
          onChange={(e) => setResumen(e.target.value)}
        />
      </div>
      <button type="submit">Crear Caso</button>
    </form>
  );
};

export default FormularioCrearCaso;