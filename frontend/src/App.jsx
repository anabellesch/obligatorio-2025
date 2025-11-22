import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
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

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Home />} />
        <Route path="/ubicacion" element={<UbicacionSalas />} />
        <Route path="/salas" element={<SalasDisponibles />} />
        <Route path="/reservas" element={<Reservas />} />
        <Route path="/reglamentacion" element={<Reglamentacion />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/asistencia" element={<AsistenciaRemota />} />
        
        {/* Rutas de administración */}
        <Route path="/admin/participantes" element={<AdminParticipantes />} />
        <Route path="/admin/reservas" element={<AdminReservas />} />
        <Route path="/admin/salas" element={<AdminSalas />} />

      </Routes>
    </Router>
  );
}

export default App;