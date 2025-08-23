// frontend/src/componentes/ListaCasos/ListaCasos.jsx
import React from 'react';
import './ListaCasos.css';

/**
 * Muestra la lista de casos.
 * AHORA PASA EL OBJETO 'caso' COMPLETO AL HACER CLIC.
 */
const ListaCasos = ({ casos, onSeleccionarCaso, casoActivoId }) => {
  return (
    <div className="lista-casos-contenedor">
      <h2>Casos Creados</h2>
      {casos && casos.length > 0 ? (
        <ul className="lista-casos">
          {casos.map((caso) => (
            // Agregamos una comprobación para asegurarnos de que 'caso' no sea undefined
            caso && (
              <li 
                key={caso.id_caso} 
                className={`caso-item ${caso.id_caso === casoActivoId ? 'activo' : ''}`}
                // --- ¡LA CORRECCIÓN CLAVE ESTÁ AQUÍ! ---
                // Le pasamos el objeto 'caso' completo a la función del padre.
                onClick={() => onSeleccionarCaso(caso)}
              >
                {caso.titulo}
              </li>
            )
          ))}
        </ul>
      ) : (
        <p>Aún no has creado ningún caso.</p>
      )}
    </div>
  );
};

export default ListaCasos;