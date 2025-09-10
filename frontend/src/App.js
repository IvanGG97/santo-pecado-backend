import './App.css';
import TareaPagina from './pages/cajaPagina/TareaPagina'
import NavBar from './components/navbar/NavBar';
import FormTarea from './pages/formTarea/FormTarea';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <NavBar />
        <Routes>
          <Route path='/' element={<TareaPagina />} />
          <Route path='/crear' element={<FormTarea />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
