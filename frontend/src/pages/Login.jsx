import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";
import "../styles/Auth.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await api.post("/auth/login", { email, password });
      
      // Guardar datos del usuario en localStorage
      const userData = {
        token: response.token,
        ci: response.user.ci,
        nombre: response.user.nombre,
        apellido: response.user.apellido,
        email: response.user.email,
        roles_academicos: response.user.roles_academicos
      };
      localStorage.setItem("user", JSON.stringify(userData));
      localStorage.setItem("token", response.token);
      
      // Redirigir al home
      navigate("/");
    } catch (err) {
      setError(err.message || "Error al iniciar sesión");
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
          <p>Iniciar Sesión</p>
        </div>

        <form onSubmit={handleLogin} className="auth-form">
          {error && (
            <div className="auth-error">
              <span>⚠️</span>
              <p>{error}</p>
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email">Correo Electrónico</label>
            <input
              id="email"
              type="email"
              placeholder="ejemplo@ucu.edu.uy"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <button 
            type="submit" 
            className="auth-button"
            disabled={loading}
          >
            {loading ? "Iniciando sesión..." : "Iniciar Sesión"}
          </button>
        </form>

        <div className="auth-footer">
          <p>¿No tienes cuenta?</p>
          <button 
            onClick={() => navigate("/register")}
            className="auth-link-button"
            disabled={loading}
          >
            Registrarse aquí
          </button>
        </div>

        {/* Credenciales de prueba */}
        <div className="auth-demo-credentials">
          <h4>👤 Credenciales de Prueba</h4>
          <div className="demo-credential">
            <strong>Administrador:</strong>
            <code>admin@ucu.edu.uy / admin123</code>
          </div>
        </div>
      </div>
    </div>
  );
}