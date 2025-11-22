import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Dashboard() {
  const [salas, setSalas] = useState([]);
  const [reservas, setReservas] = useState([]);
  const [participantes, setParticipantes] = useState([]);
  const [sanciones, setSanciones] = useState([]);
  const [reportes, setReportes] = useState({});

  useEffect(() => {
    api.get("/salas/").then(setSalas).catch(console.error);
    api.get("/reservas/").then(setReservas).catch(console.error);
    api.get("/participantes/").then(setParticipantes).catch(console.error);
    api.get("/sanciones/").then(setSanciones).catch(console.error);
    api.get("/reportes/estadisticas").then(setReportes).catch(console.error);
  }, []);

  return (
    <div className="page">
      <h2>Dashboard</h2>

      <section>
        <h3>Estadísticas generales</h3>
        <pre>{JSON.stringify(reportes, null, 2)}</pre>
      </section>

      <section>
        <h3>Salas ({salas.length})</h3>
        <ul>
          {salas.map((s) => (
            <li key={s.id_sala}>{s.nombre_sala} - {s.edificio || s.nombre_edificio || s.id_edificio} ({s.capacidad})</li>
          ))}
        </ul>
      </section>

      <section>
        <h3>Reservas ({reservas.length})</h3>
        <ul>
          {reservas.slice(0,20).map((r) => (
            <li key={r.id_reserva}>{r.id_reserva} - Sala: {r.id_sala || r.nombre_sala} - {r.fecha} - Turno: {r.id_turno}</li>
          ))}
        </ul>
      </section>

      <section>
        <h3>Participantes ({participantes.length})</h3>
        <ul>
          {participantes.slice(0,20).map((p) => (
            <li key={p.ci}>{p.ci} - {p.nombre} {p.apellido} ({p.email})</li>
          ))}
        </ul>
      </section>

      <section>
        <h3>Sanciones ({sanciones.length})</h3>
        <ul>
          {sanciones.slice(0,20).map((s) => (
            <li key={s.id_sancion}>{s.ci_participante} - {s.fecha_inicio} to {s.fecha_fin} - {s.motivo}</li>
          ))}
        </ul>
      </section>
    </div>
  );
}
