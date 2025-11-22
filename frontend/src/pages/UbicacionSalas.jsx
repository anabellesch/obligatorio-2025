import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function UbicacionSalas() {
  const [salas, setSalas] = useState([]);

  useEffect(() => {
    api.get("/salas").then(setSalas).catch(console.error);
  }, []);

  return (
    <div className="page">
      <h2>Ubicación de Salas</h2>
      <table>
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Edificio</th>
            <th>Capacidad</th>
            <th>Tipo</th>
          </tr>
        </thead>
        <tbody>
          {salas.map((sala) => (
            <tr key={sala.nombre_sala}>
              <td>{sala.nombre_sala}</td>
              <td>{sala.edificio}</td>
              <td>{sala.capacidad}</td>
              <td>{sala.tipo_sala}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
