import { useEffect, useState } from "react";
import { api } from "../../services/api";

export default function AdminParticipantes() {
  const [lista, setLista] = useState([]);
  const [filter, setFilter] = useState('reservantes'); // 'reservantes' | 'all'
  const [form, setForm] = useState({ci:'', nombre:'', apellido:'', email:''});

  const fetchAll = async () => {
    try {
      const endpoint = filter === 'reservantes' ? '/participantes/reservantes' : '/participantes/';
      const res = await api.get(endpoint);
      setLista(res);
    } catch (e) { alert(e.message) }
  };

  useEffect(()=>{ fetchAll(); }, [filter]);

  const handleCreate = async () => {
    try {
      // Debug: show payload and built URL in console to diagnose 'Failed to fetch'
      try { console.debug('[AdminParticipantes] creating', form); } catch (e) {}
      await api.post("/participantes/", form);
      setForm({ci:'', nombre:'', apellido:'', email:''});
      fetchAll();
    } catch (e) { alert(e.message) }
  };

  const handleDelete = async (ci) => {
    if (!window.confirm("Eliminar participante?")) return;
    await api.del(`/participantes/${ci}`);
    fetchAll();
  };

  return (
    <div>
      <h3>ABM Participantes</h3>
      <div className="form">
        <input placeholder="CI" value={form.ci} onChange={e=>setForm({...form, ci:e.target.value})} />
        <input placeholder="Nombre" value={form.nombre} onChange={e=>setForm({...form, nombre:e.target.value})} />
        <input placeholder="Apellido" value={form.apellido} onChange={e=>setForm({...form, apellido:e.target.value})} />
        <input placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} />
        <button onClick={handleCreate}>Crear</button>
      </div>

      <div style={{ marginTop: 12 }}>
        <label style={{ marginRight: 8 }}>Ver:</label>
        <button onClick={() => setFilter('reservantes')} style={{ marginRight: 8, fontWeight: filter==='reservantes'? 'bold':'normal' }}>Con reservas</button>
        <button onClick={() => setFilter('all')} style={{ fontWeight: filter==='all'? 'bold':'normal' }}>Todos</button>
      </div>

      <table>
        <thead><tr><th>CI</th><th>Nombre</th><th>Email</th><th>Reservas</th><th></th></tr></thead>
        <tbody>
          {lista.map(p => (
            <tr key={p.ci}>
              <td>{p.ci}</td>
              <td>{p.nombre} {p.apellido}</td>
              <td>{p.email}</td>
              <td>{p.reservas_count ?? '-'}</td>
              <td><button onClick={()=>handleDelete(p.ci)}>Eliminar</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
