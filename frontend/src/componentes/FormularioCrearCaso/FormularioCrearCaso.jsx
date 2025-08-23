// frontend/src/componentes/FormularioCrearCaso/FormularioCrearCaso.jsx

import React, { useState } from 'react';
import { crearNuevoCaso } from '../../servicios/api';
import './FormularioCrearCaso.css';

const FormularioCrearCaso = ({ onCasoCreado }) => {
  const [titulo, setTitulo] = useState('');
  const [resumen, setResumen] = useState('');
  const [estaCreando, setEstaCreando] = useState(false);

  const manejarEnvio = async (evento) => {
    evento.preventDefault();
    if (!titulo.trim()) {
      alert("El título del caso no puede estar vacío.");
      return;
    }
    setEstaCreando(true);
    try {
      const nuevoCaso = await crearNuevoCaso(titulo, resumen);
      onCasoCreado(nuevoCaso);
      setTitulo('');
      setResumen('');
    } catch (error) { // La variable 'error' se captura aquí
      // --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---
      // Ahora usamos la variable 'error' para mostrar más detalles en la consola.
      // Esto elimina la advertencia y mejora nuestra capacidad de depuración.
      console.error("Detalles del error al crear el caso:", error);
      alert("Hubo un error al crear el caso. Revisa la consola para más detalles.");
    } finally {
      setEstaCreando(false);
    }
  };

  return (
    <div className="formulario-crear-caso-contenedor">
      <h3>Crear Nuevo Caso</h3>
      <form onSubmit={manejarEnvio} className="formulario-crear-caso">
        <div className="grupo-formulario">
          <label htmlFor="titulo-caso">Título del Caso</label>
          <input
            id="titulo-caso"
            type="text"
            value={titulo}
            onChange={(e) => setTitulo(e.target.value)}
            placeholder="Ej: Accidente de tránsito Pérez"
            required
          />
        </div>
        <div className="grupo-formulario">
          <label htmlFor="resumen-caso">Resumen Preliminar</label>
          <textarea
            id="resumen-caso"
            value={resumen}
            onChange={(e) => setResumen(e.target.value)}
            placeholder="Breve descripción de los hechos..."
          />
        </div>
        <button type="submit" disabled={estaCreando || !titulo}>
          {estaCreando ? 'Creando...' : 'Crear Caso'}
        </button>
      </form>
    </div>
  );
};

export default FormularioCrearCaso;