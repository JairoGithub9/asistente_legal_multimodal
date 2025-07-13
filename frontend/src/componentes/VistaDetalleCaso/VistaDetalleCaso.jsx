// frontend/src/componentes/VistaDetalleCaso/VistaDetalleCaso.jsx
import './VistaDetalleCaso.css';

// Este componente recibe el caso seleccionado como un "prop"
const VistaDetalleCaso = ({ casoSeleccionado }) => {
  // Si no hay ningún caso seleccionado, no mostramos nada.
  if (!casoSeleccionado) {
    return (
      <div className="vista-detalle-contenedor placeholder">
        <p>Selecciona un caso de la lista para ver sus detalles.</p>
      </div>
    );
  }

  // Si el caso está seleccionado, mostramos toda su información.
  return (
    <div className="vista-detalle-contenedor">
      <h2>Detalle del Caso: {casoSeleccionado.titulo}</h2>
      <p><strong>Resumen:</strong> {casoSeleccionado.resumen || 'No proporcionado'}</p>
      <p><strong>ID:</strong> {casoSeleccionado.id_caso}</p>
      <p><strong>Fecha de Creación:</strong> {new Date(casoSeleccionado.fecha_creacion).toLocaleString()}</p>
      
      <hr />

      <h3>Evidencias ({casoSeleccionado.evidencias.length})</h3>
      {casoSeleccionado.evidencias.length === 0 ? (
        <p>Este caso no tiene evidencias todavía.</p>
      ) : (
        casoSeleccionado.evidencias.map(evidencia => (
          <div key={evidencia.id_evidencia} className="evidencia-card">
            <h4>Archivo: {evidencia.nombre_archivo}</h4>
            <p><strong>Estado:</strong> {evidencia.estado_procesamiento}</p>
            
            {evidencia.texto_extraido && (
              <div className="detalle-seccion">
                <h5>Texto Extraído</h5>
                <p className="texto-contenido">{evidencia.texto_extraido}</p>
              </div>
            )}

            {evidencia.entidades_extraidas && (
              <div className="detalle-seccion">
                <h5>Entidades Clave</h5>
                <ul>
                  {evidencia.entidades_extraidas.map((ent, index) => (
                    <li key={index}><strong>{ent.entidad}</strong> ({ent.tipo})</li>
                  ))}
                </ul>
              </div>
            )}
            
            {evidencia.informacion_recuperada && (
              <div className="detalle-seccion">
                <h5>Información Recuperada (RAG)</h5>
                {evidencia.informacion_recuperada.map((info, index) => (
                  <p key={index} className="texto-contenido">{info}</p>
                ))}
              </div>
            )}

            {evidencia.borrador_estrategia && (
              <div className="detalle-seccion estrategia">
                <h5>Borrador de Estrategia</h5>
                <pre>{evidencia.borrador_estrategia}</pre>
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );
};

export default VistaDetalleCaso;