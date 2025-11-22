import { useNavigate, useLocation } from "react-router-dom";
import { useState, useEffect } from "react";
import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Cargar usuario del localStorage
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    setUser(null);
    navigate("/login");
  };

  // No mostrar navbar en la página de login
  if (location.pathname === "/login") {
    return null;
  }

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <img 
          src='https://logoteca.uy/wp-content/uploads/sites/3/2024/09/Logo-Universidad-Catolica.svg' 
          alt="Logo UCU" 
          className="logo" 
        />
        <div className="navbar-title">
          <p>Universidad Católica del Uruguay</p>
        </div>
      </div>

      <div className="navbar-right">
        {user ? (
          <div className="user-menu">
            <span className="user-name">
              👤 {user.nombre} {user.apellido}
            </span>
            <button className="btn-logout" onClick={handleLogout}>
              Cerrar Sesión
            </button>
          </div>
        ) : (
          <button className="btn-login-navbar" onClick={() => navigate("/login")}>
            Iniciar Sesión
          </button>
        )}
      </div>
    </nav>
  );
}

export default Navbar;