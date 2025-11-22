import { useState, useEffect } from "react";
import { api } from "../services/api";
import Navbar from "../components/Navbar";
import "../styles/Salas.css";

export default function SalasDisponibles() {
  const [fecha, setFecha] = useState("");
  const [idTurno, setIdTurno] = useState("");
  const [turnos, setTurnos] = useState([]);
  const [salas, setSalas] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false);

  // Cargar turnos al montar el componente
  useEffect(() => {
    loadTurnos();
  }, []);

  const loadTurnos = async () => {
    try {
      const data = await api.get("/api/salas/turnos");
      setTurnos(data);
    } catch (err) {
      console.error("Error cargando turnos:", err);
      setError("Error al cargar los horarios disponibles");
    }
  };

  const buscarSalas = async () => {
    if (!fecha || !idTurno) {
      setError("Por favor selecciona una fecha y un turno");
      return;
    }

    setLoading(true);
    setError("");
    setSearched(true);

    try {
      const data = await api.post("/api/salas/disponibles", {
        fecha,
        id_turno: idTurno
      });
      setSalas(data);
    } catch (err) {
      console.error("Error buscando salas:", err);
      setError("Error al buscar salas disponibles");
      setSalas([]);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (timeStr) => {
    if (!timeStr) return "";
    return timeStr.substring(0, 5); // HH:MM
  };

  return (
    <div className="page-container">
      <Navbar />
      
      <div className="page salas-page">
        <h2>Salas Disponibles</h2>
        <p className="subtitle">
          Busca salas disponibles seleccionando una fecha y un horario
        </p>

        {/* Filtros de búsqueda */}
        <div className="filtros-container">
          <div className="filtro-group">
            <label htmlFor="fecha">Fecha</label>
            <input
              id="fecha"
              type="date"
              className="input-filtro"
              value={fecha}
              onChange={(e) => setFecha(e.target.value)}
              min={new Date().toISOString().split('T')[0]}
            />
          </div>

          <div className="filtro-group">
            <label htmlFor="turno">Horario</label>
            <select
              id="turno"
              className="input-filtro"
              value={idTurno}
              onChange={(e) => setIdTurno(e.target.value)}
            >
              <option value="">Selecciona un horario</option>
              {turnos.map((turno) => (
                <option key={turno.id_turno} value={turno.id_turno}>
                  {formatTime(turno.hora_inicio)} - {formatTime(turno.hora_fin)}
                </option>
              ))}
            </select>
          </div>

          <button
            className="btn-buscar"
            onClick={buscarSalas}
            disabled={loading}
          >
            {loading ? "Buscando..." : "Buscar"}
          </button>
        </div>

        {/* Mensajes de error */}
        {error && <div className="error-message">{error}</div>}

        {/* Resultados */}
        {searched && !loading && (
          <div className="resultados-container">
            <h3>
              {salas.length > 0
                ? `Se encontraron ${salas.length} sala(s) disponible(s)`
                : "No hay salas disponibles para la fecha y horario seleccionados"}
            </h3>

            {salas.length > 0 && (
              <div className="salas-grid">
                {salas.map((sala) => (
                  <div key={sala.id_sala} className="sala-card">
                    <div className="sala-header">
                      <h4>{sala.nombre_sala}</h4>
                      <span className={`tipo-badge tipo-${sala.tipo_sala}`}>
                        {sala.tipo_sala}
                      </span>
                    </div>
                    
                    <div className="sala-info">
                      <div className="info-item">
                        <span className="icon">📍</span>
                        <div>
                          <strong>{sala.nombre_edificio}</strong>
                          <p>{sala.direccion}</p>
                        </div>
                      </div>
                      
                      <div className="info-item">
                        <span className="icon">👥</span>
                        <div>
                          <strong>Capacidad</strong>
                          <p>{sala.capacidad} personas</p>
                        </div>
                      </div>
                    </div>

                    <button className="btn-reservar">
                      Reservar
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}