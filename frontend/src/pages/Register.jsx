import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";
import "../styles/Auth.css";

export default function Register() {
  const [formData, setFormData] = useState({
    ci: "",
    nombre: "",
    apellido: "",
    email: "",
    password: "",
    confirmPassword: "",
    
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");

    // Validaciones
    if (formData.password !== formData.confirmPassword) {
      setError("Las contraseñas no coinciden");
      return;
    }

    if (formData.password.length < 6) {
      setError("La contraseña debe tener al menos 6 caracteres");
      return;
    }

    if (formData.ci.length < 7) {
      setError("La cédula debe tener al menos 7 dígitos");
      return;
    }

    setLoading(true);

    try {
      const { confirmPassword, ...dataToSend } = formData;
      // Enviar registro y mostrar respuesta en consola para depuración
      const resp = await api.post("/auth/register", dataToSend);
      try { console.debug('Register response (backend):', resp); } catch (e) {}
      // Mostrar mensaje de éxito y redirigir al login
      alert("¡Registro exitoso! Ahora puedes iniciar sesión.");
      navigate("/login");
    } catch (err) {
      setError(err.message || "Error al registrarse");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <div className="auth-header">
          <img 
            src='https://logoteca.uy/wp-content/uploads/sites/3/2024/09/Logo-Universidad-Catolica.svg' 
            alt="Logo UCU" 
            className="auth-logo"
          />
          <h2>Sistema de Gestión de Salas</h2>
          <p>Crear Nueva Cuenta</p>
        </div>

        <form onSubmit={handleRegister} className="auth-form">
          {error && (
            <div className="auth-error">
              <span>⚠️</span>
              <p>{error}</p>
            </div>
          )}

          <div className="form-group">
            <label htmlFor="ci">Cédula de Identidad</label>
            <input
              id="ci"
              name="ci"
              type="text"
              placeholder="12345678"
              value={formData.ci}
              onChange={handleChange}
              required
              disabled={loading}
              maxLength="8"
            />
          </div>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
            <div className="form-group">
              <label htmlFor="nombre">Nombre</label>
              <input
                id="nombre"
                name="nombre"
                type="text"
                placeholder="Juan"
                value={formData.nombre}
                onChange={handleChange}
                required
                disabled={loading}
              />
            </div>

            <div className="form-group">
              <label htmlFor="apellido">Apellido</label>
              <input
                id="apellido"
                name="apellido"
                type="text"
                placeholder="Pérez"
                value={formData.apellido}
                onChange={handleChange}
                required
                disabled={loading}
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="email">Correo Electrónico</label>
            <input
              id="email"
              name="email"
              type="email"
              placeholder="ejemplo@ucu.edu.uy"
              value={formData.email}
              onChange={handleChange}
              required
              disabled={loading}
            />
          </div>

          

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "16px" }}>
            <div className="form-group">
              <label htmlFor="password">Contraseña</label>
              <input
                id="password"
                name="password"
                type="password"
                placeholder="••••••••"
                value={formData.password}
                onChange={handleChange}
                required
                disabled={loading}
                minLength="6"
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirmPassword">Confirmar Contraseña</label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                placeholder="••••••••"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                disabled={loading}
                minLength="6"
              />
            </div>
          </div>

          <button 
            type="submit" 
            className="auth-button"
            disabled={loading}
          >
            {loading ? "Registrando..." : "Crear Cuenta"}
          </button>
        </form>

        <div className="auth-footer">
          <p>¿Ya tienes cuenta?</p>
          <button 
            onClick={() => navigate("/login")}
            className="auth-link-button"
            disabled={loading}
          >
            Iniciar sesión aquí
          </button>
        </div>
      </div>
    </div>
  );
}