// frontend/src/App.jsx
import { useState, useEffect, useCallback } from 'react'; // 1. Importamos useCallback
import './App.css';
import ListaCasos from './componentes/ListaCasos/ListaCasos';
import VistaDetalleCaso from './componentes/VistaDetalleCaso/VistaDetalleCaso';
import FormularioCrearCaso from './componentes/FormularioCrearCaso/FormularioCrearCaso';
import { obtenerTodosLosCasos } from './servicios/api';

function App() {
  const [casos, setCasos] = useState([]);
  const [casoSeleccionado, setCasoSeleccionado] = useState(null);

  // --- 2. ENVOLVEMOS LA FUNCIÓN EN useCallback ---
  /**
   * Esta función ahora está "memorizada" por React. Solo se creará una nueva
   * versión de esta función si su dependencia (`casoSeleccionado`) cambia.
   * Esto resuelve el bug de las "funciones viejas" en los re-renders.
   */
  const recargarDatos = useCallback(async () => {
    console.log("APP: Recargando todos los datos desde la API...");
    const datosActualizados = await obtenerTodosLosCasos();
    setCasos(datosActualizados);

    // Si había un caso seleccionado, también actualizamos sus datos
    if (casoSeleccionado) {
      const casoRefrescado = datosActualizados.find(c => c.id_caso === casoSeleccionado.id_caso);
      setCasoSeleccionado(casoRefrescado);
    }
  }, [casoSeleccionado]); // 3. Le decimos a useCallback que depende de `casoSeleccionado`
  
  useEffect(() => {
    recargarDatos();
  }, [recargarDatos]); // Ahora la dependencia de useEffect es la propia función memorizada

  const manejarSeleccionCaso = (caso) => {
    setCasoSeleccionado(caso);
  };

  const manejarCasoCreado = async (nuevoCaso) => {
    console.log("APP: Nuevo caso creado. Refrescando la lista de casos.");
    await recargarDatos();
    
    // Después de recargar, la nueva lista de 'casos' contendrá el nuevo caso.
    // Lo buscamos para asegurarnos de tener el objeto más actualizado.
    const casoRecienCreado = await obtenerTodosLosCasos().then(lista => lista.find(c => c.id_caso === nuevoCaso.id_caso));
    setCasoSeleccionado(casoRecienCreado);
  };
  
  return (
    <div className="app-contenedor">
      <header>
        <h1>Asistente Legal Multimodal</h1>
      </header>
      <main className="main-layout">
        <div className="columna-izquierda">
          <FormularioCrearCaso onCasoCreado={manejarCasoCreado} />
          <ListaCasos 
            casos={casos} 
            onSeleccionarCaso={manejarSeleccionCaso} 
            casoActivoId={casoSeleccionado ? casoSeleccionado.id_caso : null}
          />
        </div>
        <div className="columna-derecha">
          <VistaDetalleCaso 
            casoSeleccionado={casoSeleccionado}
            // Pasamos la función memorizada a los hijos
            onEvidenciaSubida={recargarDatos}
            onAnalisisCompleto={recargarDatos}
          />
        </div>
      </main>
    </div>
  );
}

export default App;