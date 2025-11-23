import { useState, useEffect } from "react";
import { api } from "../services/api";
import Navbar from "../components/Navbar";
import "../styles/Salas.css";

export default function Reservas() {
  const [reservas, setReservas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadReservas();
  }, []);

  const loadReservas = async () => {
    try {
      setLoading(true);
      const data = await api.get("/api/reservas");
      setReservas(data);
    } catch (err) {
      console.error("Error cargando reservas:", err);
      setError("Error al cargar las reservas");
    } finally {
      setLoading(false);
    }
  };

  const cancelarReserva = async (id_reserva) => {
    if (!confirm('¿Confirma cancelar esta reserva?')) return;
    try {
      await api.del(`/reservas/${id_reserva}`);
      await loadReservas();
      alert('Reserva cancelada');
    } catch (err) {
      console.error('Error cancelando reserva:', err);
      alert(err.message || 'No se pudo cancelar la reserva');
    }
  };

  const getEstadoBadgeClass = (estado) => {
    const classes = {
      activa: "estado-activa",
      cancelada: "estado-cancelada",
      finalizada: "estado-finalizada",
      "sin asistencia": "estado-sin-asistencia"
    };
    return classes[estado] || "";
  };

  if (loading) {
    return (
      <div className="page-container">
        <Navbar />
        <div className="page">
          <div className="loading-message">Cargando reservas...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <Navbar />
      
      <div className="page salas-page">
        <h2>Mis Reservas</h2>
        <p className="subtitle">
          Administra tus reservas de salas de estudio
        </p>

        {error && <div className="error-message">{error}</div>}

        <div className="stats-container">
          <div className="stat-card">
            <span className="stat-number">
              {reservas.filter(r => r.estado === 'activa').length}
            </span>
            <span className="stat-label">Activas</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">
              {reservas.filter(r => r.estado === 'finalizada').length}
            </span>
            <span className="stat-label">Finalizadas</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">{reservas.length}</span>
            <span className="stat-label">Total</span>
          </div>
        </div>

        <div className="table-container">
          {reservas.length === 0 ? (
            <div style={{ textAlign: "center", padding: "40px" }}>
              <p style={{ color: "#666", fontSize: "16px" }}>
                No tienes reservas registradas
              </p>
            </div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Sala</th>
                  <th>Fecha</th>
                  <th>Turno</th>
                  <th>Estado</th>
                  <th>Fecha Solicitud</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {reservas.map((reserva) => (
                  <tr key={reserva.id_reserva}>
                    <td>#{reserva.id_reserva}</td>
                    <td>
                      <strong>Sala {reserva.id_sala}</strong>
                    </td>
                    <td>
                      {(() => {
                        // reserva.fecha comes as 'YYYY-MM-DD' (no time). Construct as local date
                        const d = reserva.fecha;
                        if (!d) return "";
                        const ymd = /^\d{4}-\d{2}-\d{2}$/.test(d);
                        if (ymd) {
                          const [y, m, day] = d.split("-");
                          return new Date(parseInt(y), parseInt(m) - 1, parseInt(day)).toLocaleDateString('es-UY');
                        }

                        const dt = new Date(d);
                        const y2 = dt.getUTCFullYear();
                        const m2 = dt.getUTCMonth();
                        const day2 = dt.getUTCDate();

                        const formatted = new Date(y2, m2, day2).toLocaleDateString('es-UY');
                        return (
                          <div>
                            <div>{formatted}</div>
                            <small style={{ color: '#666' }}>{String(d)}</small>
                          </div>
                        );
                      })()}
                    </td>
                    <td>Turno {reserva.id_turno}</td>
                    <td>
                      <span className={`estado-badge ${getEstadoBadgeClass(reserva.estado)}`}>
                        {reserva.estado}
                      </span>
                    </td>
                    <td>
                      {reserva.fecha_solicitud ? new Date(reserva.fecha_solicitud).toLocaleString('es-UY') : ''}
                    </td>
                    <td>
                      <button className="btn-cancel" onClick={() => cancelarReserva(reserva.id_reserva)}>
                        Cancelar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}