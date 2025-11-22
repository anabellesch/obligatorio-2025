import { useEffect, useState } from "react";
import { api } from "../../services/api";

export default function AdminReservas() {
  const [salas, setSalas] = useState([]);
  const [turnos, setTurnos] = useState([]);
  const [reservas, setReservas] = useState([]);
  const [form, setForm] = useState({id_sala:'', fecha:'', id_turno:'', ci_solicitante:''});

  useEffect(()=>{ fetchInitial(); }, []);

  const fetchInitial = async () => {
    try {
      const s = await api.get("/salas");
      setSalas(s);
      const t = await api.get("/turnos");
      setTurnos(t);
      const r = await api.get("/reservas");
      setReservas(r);
    } catch (e) { console.error(e) }
  };

  const crearReserva = async () => {
    try {
      await api.post("/reservas", form);
      alert("Reserva creada");
      fetchInitial();
    } catch (e) {
      alert(e.message);
    }
  };

  return (
    <div>
      <h3>Reservas</h3>
      <div className="form">
        <select onChange={e=>setForm({...form, id_sala:e.target.value})}>
          <option value="">Elegir sala</option>
          {salas.map(s=> <option value={s.id_sala} key={s.id_sala}>{s.nombre_sala} - {s.nombre_edificio}</option>)}
        </select>
        <input type="date" onChange={e=>setForm({...form, fecha:e.target.value})}/>
        <select onChange={e=>setForm({...form, id_turno:e.target.value})}>
          <option value="">Elegir turno</option>
          {turnos.map(t=> <option value={t.id_turno} key={t.id_turno}>{t.hora_inicio} - {t.hora_fin}</option>)}
        </select>
        <input placeholder="CI solicitante" onChange={e=>setForm({...form, ci_solicitante:e.target.value})}/>
        <button onClick={crearReserva}>Crear</button>
      </div>

      <h4>Reservas existentes</h4>
      <table>
        <thead><tr><th>Id</th><th>Sala</th><th>Fecha</th><th>Turno</th><th>Estado</th></tr></thead>
        <tbody>
          {reservas.map(r=>(
            <tr key={r.id_reserva}>
              <td>{r.id_reserva}</td>
              <td>{r.nombre_sala}</td>
              <td>{r.fecha}</td>
              <td>{r.hora_inicio} - {r.hora_fin}</td>
              <td>{r.estado}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
