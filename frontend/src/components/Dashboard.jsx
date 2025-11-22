import { useEffect, useState } from 'react';
import { api } from '../services/api';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [reservas, setReservas] = useState([]);
  const [salas, setSalas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const reservasData = await api.get('/reservas/');
        const salasData = await api.get('/salas/');
        setReservas(reservasData);
        setSalas(salasData);
      } catch (err) {
        setError('Error al cargar datos');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const total = reservas.length;
  const active = reservas.filter(r => r.estado === 'activa').length;

  const today = (() => {
    const t = new Date();
    t.setHours(0,0,0,0);
    return t;
  })();

  const upcoming = reservas
    .filter(r => r.estado === 'activa')
    .map(r => ({ ...r, dateObj: new Date(r.fecha) }))
    .filter(r => r.dateObj >= today)
    .sort((a,b) => a.dateObj - b.dateObj)
    .slice(0,5);

  const salaById = {};
  salas.forEach(s => { salaById[s.id_sala] = s; });

  return (
    <div className="dashboard">
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Panel de Control</h2>
        <div>
          <button onClick={() => navigate('/reservas')} style={{ marginRight: 8 }}>Mis Reservas</button>
          <button onClick={() => navigate('/salas')}>Ver Salas</button>
        </div>
      </header>

      {error && <div style={{ color: 'red' }}>{error}</div>}

      <section style={{ display: 'flex', gap: 12, marginTop: 16 }}>
        <div style={{ padding: 16, background: '#fff', borderRadius: 8, boxShadow: '0 1px 3px rgba(0,0,0,0.1)', flex: 1 }}>
          <h4>Total Reservas</h4>
          <div style={{ fontSize: 28, fontWeight: 'bold' }}>{total}</div>
        </div>
        <div style={{ padding: 16, background: '#fff', borderRadius: 8, boxShadow: '0 1px 3px rgba(0,0,0,0.1)', flex: 1 }}>
          <h4>Activas</h4>
          <div style={{ fontSize: 28, fontWeight: 'bold' }}>{active}</div>
        </div>
        <div style={{ padding: 16, background: '#fff', borderRadius: 8, boxShadow: '0 1px 3px rgba(0,0,0,0.1)', flex: 2 }}>
          <h4>Próximas Reservas</h4>
          {loading ? <div>Cargando...</div> : (
            upcoming.length === 0 ? <div>No hay próximas reservas</div> : (
              <ul style={{ paddingLeft: 0, listStyle: 'none' }}>
                {upcoming.map(r => (
                  <li key={r.id_reserva} style={{ padding: '8px 0', borderBottom: '1px solid #eee' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <div>
                        <strong>{salaById[r.id_sala]?.nombre_sala || `Sala ${r.id_sala}`}</strong>
                        <div style={{ fontSize: 12, color: '#666' }}>{new Date(r.fecha).toLocaleDateString('es-UY')}</div>
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <div>Turno {r.id_turno}</div>
                        <button onClick={() => navigate('/reservas')} style={{ marginTop: 6 }}>Ver</button>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )
          )}
        </div>
      </section>

    </div>
  );
}

export default Dashboard;
