// frontend/src/componentes/VistaDetalleCaso/VistaDetalleCaso.jsx

import React, { useState, useEffect } from 'react';
import './VistaDetalleCaso.css';
import FormularioSubirEvidencia from '../FormularioSubirEvidencia/FormularioSubirEvidencia';
import { subirEvidencia, obtenerEstadoEvidencia } from '../../servicios/api';

const VistaDetalleCaso = ({ casoSeleccionado, onEvidenciaSubida, onAnalisisCompleto }) => {
  const [idEvidenciaEnSondeo, setIdEvidenciaEnSondeo] = useState(null);
  const [estaProcesando, setEstaProcesando] = useState(false);

  const manejarSubidaDeArchivo = async (archivo) => {
    if (!casoSeleccionado) return;
    setEstaProcesando(true);
    try {
      const casoActualizado = await subirEvidencia(casoSeleccionado.id_caso, archivo);
      const nuevaEvidencia = casoActualizado.evidencias[casoActualizado.evidencias.length - 1];
      onEvidenciaSubida(casoActualizado); // Le avisamos al padre para que muestre la evidencia "encolada"
      setIdEvidenciaEnSondeo(nuevaEvidencia.id_evidencia);
    } catch (error) {
      console.error("Error en el proceso de subida:", error);
      setEstaProcesando(false);
    }
  };

  useEffect(() => {
    if (!idEvidenciaEnSondeo) return;

    const intervalo = setInterval(async () => {
      const respuesta = await obtenerEstadoEvidencia(idEvidenciaEnSondeo);
      const estadoActual = respuesta.estado_procesamiento;

      if (estadoActual === 'completado' || estadoActual.includes('error')) {
        clearInterval(intervalo);
        
        // --- LA SOLUCIÓN PROFESIONAL ---
        // En lugar de recargar la página, llamamos a la función que nos pasó el padre.
        console.log("ANÁLISIS COMPLETO: Avisando al componente App para que refresque los datos.");
        onAnalisisCompleto(); // App.jsx se encargará de obtener los datos frescos.

        setIdEvidenciaEnSondeo(null);
        setEstaProcesando(false); // Desactivamos el estado de "procesando".
      }
    }, 5000);

    return () => clearInterval(intervalo);
  }, [idEvidenciaEnSondeo, onAnalisisCompleto]);

  if (!casoSeleccionado) {
    return <div className="vista-detalle-contenedor placeholder"><p>Selecciona un caso...</p></div>;
  }

  return (
    <div className="vista-detalle-contenedor">
      <h2>Detalle del Caso: {casoSeleccionado.titulo}</h2>
      <p><strong>Resumen:</strong> {casoSeleccionado.resumen || 'No proporcionado'}</p>
      <p><strong>ID:</strong> {casoSeleccionado.id_caso}</p>
      
      <hr />

      <FormularioSubirEvidencia 
        onArchivoSeleccionado={manejarSubidaDeArchivo}
        estaProcesando={estaProcesando}
      />

      <h3>Evidencias ({casoSeleccionado.evidencias.length})</h3>
      {casoSeleccionado.evidencias.map(evidencia => (
        <div key={evidencia.id_evidencia} className="evidencia-card">
          <h4>Archivo: {evidencia.nombre_archivo}</h4>
          <p><strong>Estado:</strong> {evidencia.estado_procesamiento}</p>
          
          {estaProcesando && idEvidenciaEnSondeo === evidencia.id_evidencia && (
            <p className="procesando-indicador"><strong>(Procesando en segundo plano...)</strong></p>
          )}

          {/* --- CÓDIGO RESTAURADO PARA MOSTRAR RESULTADOS --- */}
          {evidencia.estado_procesamiento === 'completado' && (
            <>
              {evidencia.texto_extraido && (
                <div className="detalle-seccion">
                  <h5>Texto Extraído</h5>
                  <pre>{evidencia.texto_extraido}</pre>
                </div>
              )}
              {evidencia.entidades_extraidas?.length > 0 && (
                <div className="detalle-seccion">
                  <h5>Entidades Clave</h5>
                  <ul>{evidencia.entidades_extraidas.map((ent, i) => <li key={i}>{ent.entidad} ({ent.categoria})</li>)}</ul>
                </div>
              )}
              {evidencia.informacion_recuperada?.length > 0 && (
                <div className="detalle-seccion">
                  <h5>Información Recuperada (RAG)</h5>
                  <pre>{evidencia.informacion_recuperada.join('\n\n')}</pre>
                </div>
              )}
              {evidencia.borrador_estrategia && (
                <div className="detalle-seccion estrategia">
                  <h5>Borrador de Estrategia</h5>
                  <pre>{evidencia.borrador_estrategia}</pre>
                </div>
              )}
              {evidencia.verificacion_calidad && (
                <div className={`detalle-seccion verificacion ${evidencia.verificacion_calidad.verificado ? 'verificado' : 'no-verificado'}`}>
                  <h5>Veredicto del Guardián de Calidad</h5>
                  <p><strong>¿Verificado?</strong> {evidencia.verificacion_calidad.verificado ? 'Sí' : 'No'}</p>
                  <p><strong>Observaciones:</strong> {evidencia.verificacion_calidad.observaciones}</p>
                </div>
              )}
            </>
          )}
        </div>
      ))}
    </div>
  );
};

export default VistaDetalleCaso;