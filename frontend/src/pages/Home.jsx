import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import "../styles/Home.css";
import "../styles/Admin.css";
import Navbar from "../components/Navbar";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      {/* Sidebar izquierdo con ícono de reloj */}
      <aside className="sidebar">
        <div className="clock-container">
          <img 
            src='https://icons.veryicon.com/png/o/miscellaneous/all-blue-icon/clock-294.png' 
            alt="Clock icon" 
            className="clock-icon"
          />
        </div>
      </aside>

      {/* Contenido principal */}
      <main className="content">
        <Navbar />

        <section className="main-section">
          <h1 className="title">Sistema de Gestión de Salas de Estudio UCU</h1>

          <div className="resources-section">
            <div className="resources-content">
              <h2 className="resources-title">RECURSOS</h2>
              
              <div className="resource-grid">
                <button 
                  className="resource-button" 
                  onClick={() => navigate("/ubicacion")}
                >
                  📍 Ubicación de salas
                </button>
                
                <button 
                  className="resource-button" 
                  onClick={() => navigate("/salas")}
                >
                  🔍 Salas disponibles
                </button>
                
                <button 
                  className="resource-button" 
                  onClick={() => navigate("/reservas")}
                >
                  📅 Mis Reservas
                </button>
                
                <button 
                  className="resource-button" 
                  onClick={() => navigate("/reglamentacion")}
                >
                  📋 Reglamentación
                </button>
                
                <button 
                  className="resource-button" 
                  onClick={() => navigate("/dashboard")}
                >
                  📊 Dashboard
                </button>
                
                <button 
                  className="resource-button" 
                  onClick={() => navigate("/asistencia")}
                >
                  💬 Asistencia remota
                </button>
              </div>

              {/* Sección de Administración */}
              <div className="admin-section">
                <h3>⚙️ ADMINISTRACIÓN</h3>
                <div className="admin-grid">
                  <button
                    className="admin-link"
                    onClick={() => navigate("/admin/participantes")}
                  >
                    👥 Participantes
                  </button>
                  
                  <button
                    className="admin-link"
                    onClick={() => navigate("/admin/salas")}
                  >
                    🏢 Salas
                  </button>
                  
                  <button
                    className="admin-link"
                    onClick={() => navigate("/admin/reservas")}
                  >
                    📋 Reservas
                  </button>
                  
                  <button
                    className="admin-link"
                    onClick={() => navigate("/admin/sanciones")}
                  >
                    ⚠️ Sanciones
                  </button>
                </div>
              </div>
            </div>

            {/* Imagen circular decorativa */}
            <div className="decorative-image-container">
              <img 
                src='https://i.pinimg.com/736x/fa/c4/20/fac420951935b4d3973acd604e43a3c0.jpg' 
                alt="Sala de estudio" 
                className="decorative-image"
              />
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}