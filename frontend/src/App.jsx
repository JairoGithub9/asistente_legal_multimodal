// frontend/src/App.jsx
import { useState, useEffect } from 'react';
import './App.css';
import { obtenerTodosLosCasos } from './servicios/api';

import FormularioCrearCaso from './componentes/FormularioCrearCaso/FormularioCrearCaso';
import ListaCasos from './componentes/ListaCasos/ListaCasos';
// ¡NUEVO! Importamos el componente de detalle
import VistaDetalleCaso from './componentes/VistaDetalleCaso/VistaDetalleCaso';

function App() {
  const [casos, setCasos] = useState([]);
  // ¡NUEVO! Estado para guardar el caso que el usuario ha seleccionado
  const [casoSeleccionado, setCasoSeleccionado] = useState(null);

  const refrescarCasos = async () => {
    const casosRecibidos = await obtenerTodosLosCasos();
    setCasos(casosRecibidos);
  };

  useEffect(() => {
    refrescarCasos();
  }, []);

  // ¡NUEVO! Esta función se llamará cuando se haga clic en un caso de la lista
  const manejarSeleccionCaso = (idCaso) => {
    const caso = casos.find(c => c.id_caso === idCaso);
    console.log("Caso seleccionado:", caso);
    setCasoSeleccionado(caso);
  };



   // ¡NUEVO! Esta función se llamará cuando se suba una evidencia
  const manejarEvidenciaSubida = (casoActualizado) => {
    // Actualizamos el caso seleccionado con la nueva información
    setCasoSeleccionado(casoActualizado);
    
    // También actualizamos la lista general de casos para mantenerla sincronizada
    setCasos(casosPrevios => casosPrevios.map(c => 
      c.id_caso === casoActualizado.id_caso ? casoActualizado : c
    ));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Asistente Legal Multimodal</h1>
      </header>
      <main className="contenedor-principal">
        <div className="columna-izquierda">
          <FormularioCrearCaso onCasoCreado={refrescarCasos} />
          <ListaCasos 
            casos={casos} 
            onSeleccionarCaso={manejarSeleccionCaso} 
            casoActivoId={casoSeleccionado?.id_caso}
          />
        </div>
        <div className="columna-derecha">
          <VistaDetalleCaso casoSeleccionado={casoSeleccionado}
          // ¡NUEVO! Pasamos la función de actualización
            onEvidenciaSubida={manejarEvidenciaSubida}
          />
          
        </div>
      </main>
    </div>
  );
}

export default App;