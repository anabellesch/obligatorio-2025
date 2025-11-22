import { useEffect, useState } from 'react';
import { getReservas, getSalas } from '../services/api';
import { useHistory } from 'react-router-dom';

function Dashboard() {
  const [reservas, setReservas] = useState([]);
  const [salas, setSalas] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const reservasData = await getReservas();
        const salasData = await getSalas();
        setReservas(reservasData);
        setSalas(salasData);
      } catch (err) {
        setError('Error al cargar datos');
      }
    };
    fetchData();
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      {error && <div>{error}</div>}
      <div>
        <h3>Reservas</h3>
        <ul>
          {reservas.map((reserva) => (
            <li key={reserva.id_reserva}>{reserva.fecha}</li>
          ))}
        </ul>
      </div>
      <div>
        <h3>Salas</h3>
        <ul>
          {salas.map((sala) => (
            <li key={sala.id_sala}>{sala.nombre_sala}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;
