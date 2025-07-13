// En ListaCasos.jsx
import './ListaCasos.css';

// Aceptamos las nuevas propiedades onSeleccionarCaso y casoActivoId
const ListaCasos = ({ casos, onSeleccionarCaso, casoActivoId }) => {
  // ... (el if de casos.length === 0 no cambia) ...

  return (
    <div className="lista-casos-contenedor">
      <h2>Casos Creados</h2>
      <ul className="lista-casos">
        {casos.map((caso) => (
          <li 
            key={caso.id_caso} 
            // Añadimos una clase si el caso es el que está activo
            className={`caso-item ${caso.id_caso === casoActivoId ? 'activo' : ''}`}
            // ¡Añadimos el evento onClick!
            onClick={() => onSeleccionarCaso(caso.id_caso)}
          >
            {caso.titulo}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ListaCasos;