// frontend/src/App.jsx

import './App.css';
// Importamos nuestro nuevo componente
import FormularioCrearCaso from './componentes/FormularioCrearCaso/FormularioCrearCaso';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Asistente Legal Multimodal</h1>
      </header>
      <main>
        <FormularioCrearCaso />
        {/* Más adelante, aquí podríamos tener otros componentes: */}
        {/* <ListaDeCasos /> */}
      </main>
    </div>
  );
}

export default App;