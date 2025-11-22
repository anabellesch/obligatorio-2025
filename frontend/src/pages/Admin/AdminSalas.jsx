import { useEffect, useState } from "react";
import { api } from "../../services/api";

export default function AdminSalas() {
  const [lista, setLista] = useState([]);
  const [form, setForm] = useState({nombre_sala:'', id_edificio:'', capacidad:10, tipo_sala:'libre'});
  const [edificios, setEdificios] = useState([]);

  const fetchAll = async () => {
    try {
      const s = await api.get("/salas");
      setLista(s);
    } catch (e) { alert(e.message) }
  };

  useEffect(()=>{ fetchAll(); }, []);

  const handleCreate = async () => {
    try {
      await api.post("/salas", {
        nombre_sala: form.nombre_sala,
        id_edificio: form.id_edificio,
        capacidad: form.capacidad,
        tipo_sala: form.tipo_sala
      });
      fetchAll();
    } catch (e) { alert(e.message) }
  };

  return (
    <div>
      <h3>ABM Salas</h3>
      <div className="form">
        <input placeholder="Nombre sala" value={form.nombre_sala} onChange={e=>setForm({...form, nombre_sala:e.target.value})} />
        <input placeholder="Id edificio" value={form.id_edificio} onChange={e=>setForm({...form, id_edificio:e.target.value})} />
        <input type="number" placeholder="Capacidad" value={form.capacidad} onChange={e=>setForm({...form, capacidad:Number(e.target.value)})} />
        <select value={form.tipo_sala} onChange={e=>setForm({...form,tipo_sala:e.target.value})}>
          <option value="libre">libre</option>
          <option value="posgrado">posgrado</option>
          <option value="docente">docente</option>
        </select>
        <button onClick={handleCreate}>Crear sala</button>
      </div>

      <table>
        <thead><tr><th>Id</th><th>Nombre</th><th>Edificio</th><th>Cap</th></tr></thead>
        <tbody>
          {lista.map(s => (
            <tr key={s.id_sala}>
              <td>{s.id_sala}</td>
              <td>{s.nombre_sala}</td>
              <td>{s.nombre_edificio}</td>
              <td>{s.capacidad}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
