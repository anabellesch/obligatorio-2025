import Navbar from "../components/Navbar";
import "../styles/Home.css";
import "../styles/Info.css";

export default function Reglamentacion() {
  return (
    <div className="page-container">
      <Navbar />
      
      <div className="page info-page">
        <h2>Reglamentación de Reservas</h2>
        <p className="subtitle">
          Normas y políticas para el uso de las salas de estudio
        </p>

        <div className="info-card">
          <h3>⏰ Límites de Tiempo</h3>
          <ul>
            <li>
              <strong>Máximo 2 horas diarias</strong> por participante en salas de uso libre
            </li>
            <li>
              Los <strong>docentes y estudiantes de posgrado</strong> pueden usar salas exclusivas sin este límite
            </li>
            <li>
              Las reservas se realizan en <strong>bloques de 1 hora</strong>
            </li>
            <li>
              Horario disponible: <strong>8:00 a 23:00 horas</strong>
            </li>
          </ul>
        </div>

        <div className="info-card">
          <h3>📅 Reservas Semanales</h3>
          <ul>
            <li>
              Máximo <strong>3 reservas activas por semana</strong> para estudiantes de grado
            </li>
            <li>
              Los docentes y estudiantes de posgrado <strong>no tienen este límite</strong>
            </li>
            <li>
              Las reservas pueden realizarse con hasta <strong>7 días de anticipación</strong>
            </li>
          </ul>
        </div>

        <div className="info-card warning">
          <h3>⚠️ Asistencia Obligatoria</h3>
          <ul>
            <li>
              La <strong>asistencia es obligatoria</strong> para todas las reservas confirmadas
            </li>
            <li>
              Debes llegar en los primeros <strong>15 minutos</strong> del turno reservado
            </li>
            <li>
              Si no puedes asistir, <strong>cancela tu reserva</strong> con al menos 2 horas de anticipación
            </li>
          </ul>
        </div>

        <div className="info-card danger">
          <h3>🚫 Sanciones</h3>
          <ul>
            <li>
              <strong>Primera falta:</strong> Advertencia formal
            </li>
            <li>
              <strong>Segunda falta:</strong> Suspensión de 30 días
            </li>
            <li>
              <strong>Tercera falta o más:</strong> Suspensión de 60 días (2 meses)
            </li>
            <li>
              Durante la sanción <strong>no se pueden realizar nuevas reservas</strong>
            </li>
          </ul>
        </div>

        <div className="info-card">
          <h3>👥 Capacidad y Participantes</h3>
          <ul>
            <li>
              El número de participantes <strong>no puede exceder la capacidad</strong> de la sala
            </li>
            <li>
              Todos los participantes deben <strong>estar registrados</strong> en la reserva
            </li>
            <li>
              Un participante sancionado <strong>no puede participar</strong> en ninguna reserva
            </li>
          </ul>
        </div>

        <div className="info-card">
          <h3>🏢 Tipos de Salas</h3>
          <ul>
            <li>
              <strong>Salas Libres:</strong> Disponibles para todos los estudiantes con las restricciones mencionadas
            </li>
            <li>
              <strong>Salas de Posgrado:</strong> Exclusivas para estudiantes de posgrado y docentes
            </li>
            <li>
              <strong>Salas de Docentes:</strong> Exclusivas para docentes
            </li>
          </ul>
        </div>

        <div className="info-card success">
          <h3>✅ Buenas Prácticas</h3>
          <ul>
            <li>
              Mantén la sala <strong>limpia y ordenada</strong>
            </li>
            <li>
              Respeta el <strong>horario de finalización</strong> para que otros puedan usar la sala
            </li>
            <li>
              <strong>Cancela</strong> las reservas que no vayas a utilizar
            </li>
            <li>
              Reporta cualquier <strong>daño o problema</strong> en la sala
            </li>
            <li>
              Mantén un <strong>ambiente de estudio tranquilo</strong>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}