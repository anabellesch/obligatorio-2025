import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import UbicacionSalas from "./pages/UbicacionSalas";
import SalasDisponibles from "./pages/SalasDisponibles";
import Reglamentacion from "./pages/ReglamentacionReservas";
import AsistenciaRemota from "./pages/AsistenciaRemota";
import Reservas from "./pages/Reservas";
import Dashboard from "./pages/Dashboard";
import AdminParticipantes from "./pages/Admin/AdminParticipantes";
import AdminReservas from "./pages/Admin/AdminReservas";
import AdminSalas from "./pages/Admin/AdminSalas";
import ProtectedRoute from "./components/ProtectedRoute";


import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Protected routes - require authentication */}
        <Route path="/" element={<ProtectedRoute><Home /></ProtectedRoute>} />
        <Route path="/ubicacion" element={<ProtectedRoute><UbicacionSalas /></ProtectedRoute>} />
        <Route path="/salas" element={<ProtectedRoute><SalasDisponibles /></ProtectedRoute>} />
        <Route path="/reservas" element={<ProtectedRoute><Reservas /></ProtectedRoute>} />
        <Route path="/reglamentacion" element={<ProtectedRoute><Reglamentacion /></ProtectedRoute>} />
        <Route path="/dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
        <Route path="/asistencia" element={<ProtectedRoute><AsistenciaRemota /></ProtectedRoute>} />
        
        {/* Rutas de administración */}
        <Route path="/admin/participantes" element={<ProtectedRoute><AdminParticipantes /></ProtectedRoute>} />
        <Route path="/admin/reservas" element={<ProtectedRoute><AdminReservas /></ProtectedRoute>} />
        <Route path="/admin/salas" element={<ProtectedRoute><AdminSalas /></ProtectedRoute>} />
      </Routes>
    </Router>
  );
}

export default App;