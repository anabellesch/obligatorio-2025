import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";

import UbicacionSalas from "./pages/UbicacionSalas";
import SalasDisponibles from "./pages/SalasDisponibles";
import Reglamentacion from "./pages/ReglamentacionReservas";
import AsistenciaRemota from "./pages/AsistenciaRemota";
import Reservas from "./pages/Reservas";
import Dashboard from "./pages/Dashboard";
import AdminParticipantes from "./pages/Admin/AdminParticipantes";
import AdminReservas from "./pages/Admin/AdminReservas";
import AdminSalas from "./pages/Admin/AdminSalas";



import "./App.css";
import { API_URL } from './services/api';

function App() {
  return (
    <Router>
      <Routes>
 
        <Route path="/" element={<Home />} />
        <Route path="/ubicacion" element={<UbicacionSalas />} />
        <Route path="/salas" element={<SalasDisponibles />} />
        <Route path="/reservas" element={<Reservas />} />
        <Route path="/reglamentacion" element={<Reglamentacion />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/asistencia" element={<AsistenciaRemota />} />

 
        <Route path="/admin/participantes" element={<AdminParticipantes />} />
        <Route path="/admin/reservas" element={<AdminReservas />} />
        <Route path="/admin/salas" element={<AdminSalas />} />
      </Routes>
      <div style={{position: 'fixed', right: 8, bottom: 8, padding: '6px 10px', background: 'rgba(0,0,0,0.6)', color: '#fff', fontSize: 12, borderRadius: 6, zIndex: 9999}}>
        API: {API_URL}
      </div>
    </Router>
  );
}

export default App;