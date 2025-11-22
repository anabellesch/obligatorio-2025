import Navbar from "../components/Navbar";
import "../styles/Home.css";
import "../styles/Info.css";

export default function AsistenciaRemota() {
  return (
    <div className="page-container">
      <Navbar />
      
      <div className="page info-page">
        <h2>Asistencia Remota</h2>
        <p className="subtitle">
          Soporte y ayuda para el sistema de gestión de salas
        </p>

        <div className="contact-grid">
          <div className="contact-card">
            <div className="contact-icon">📧</div>
            <h3>Email</h3>
            <p>
              <strong>salas@ucu.edu.uy</strong>
            </p>
            <p className="contact-description">
              Envíanos tus consultas o reportes. Responderemos en un plazo máximo de 24 horas.
            </p>
          </div>

          <div className="contact-card">
            <div className="contact-icon">📞</div>
            <h3>Teléfono</h3>
            <p>
              <strong>+598 2487 2717</strong>
            </p>
            <p className="contact-description">
              Atención telefónica de lunes a viernes de 9:00 a 18:00 horas.
            </p>
          </div>

          <div className="contact-card">
            <div className="contact-icon">🕐</div>
            <h3>Horario de Atención</h3>
            <p>
              <strong>Lunes a Viernes</strong><br />
              9:00 - 18:00 hs
            </p>
            <p className="contact-description">
              Atención presencial en la oficina de Gestión Académica.
            </p>
          </div>
        </div>

        <div className="info-card">
          <h3>💡 Preguntas Frecuentes</h3>
          
          <div className="faq-item">
            <h4>¿Cómo hago una reserva?</h4>
            <p>
              Accede a la sección "Salas Disponibles", selecciona la fecha y horario deseado, 
              y elige una sala disponible. Completa el formulario con los datos de todos los participantes.
            </p>
          </div>

          <div className="faq-item">
            <h4>¿Puedo cancelar una reserva?</h4>
            <p>
              Sí, puedes cancelar una reserva hasta 2 horas antes del turno reservado. 
              Accede a "Mis Reservas" y selecciona la opción de cancelar.
            </p>
          </div>

          <div className="faq-item">
            <h4>¿Qué hago si tengo una sanción?</h4>
            <p>
              Las sanciones se aplican automáticamente por no asistencia. Si crees que hay un error, 
              contacta con nosotros por email o teléfono con tu número de cédula y el ID de la reserva.
            </p>
          </div>

          <div className="faq-item">
            <h4>¿Puedo modificar una reserva existente?</h4>
            <p>
              Actualmente no es posible modificar una reserva. Debes cancelar la reserva actual 
              y crear una nueva con los datos correctos.
            </p>
          </div>

          <div className="faq-item">
            <h4>¿Qué hago si encuentro un problema en la sala?</h4>
            <p>
              Reporta cualquier problema (daños, falta de limpieza, equipos no funcionando) 
              inmediatamente por email o teléfono indicando el nombre de la sala y el edificio.
            </p>
          </div>
        </div>

        <div className="info-card success">
          <h3>📍 Ubicación</h3>
          <p>
            <strong>Oficina de Gestión Académica</strong><br />
            Edificio Central, Piso 2<br />
            Av. 8 de Octubre 2738<br />
            Montevideo, Uruguay
          </p>
        </div>

        <div className="info-card">
          <h3>🔧 Soporte Técnico</h3>
          <p>
            Si experimentas problemas técnicos con el sistema (errores, pantallas en blanco, 
            imposibilidad de realizar reservas), por favor contacta a:
          </p>
          <p>
            <strong>Email:</strong> soporte.ti@ucu.edu.uy<br />
            <strong>Interno:</strong> 5555
          </p>
        </div>
      </div>
    </div>
  );
}