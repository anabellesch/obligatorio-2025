import { useState } from "react";
import { api } from "../services/api";
import { useNavigate } from "react-router-dom";
import { useUser } from "../hooks/useUser";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { setUser } = useUser();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const r = await api.post("/login", { email, password });
      // Guardar en localStorage y hook
      const payload = {
        correo: r.correo,
        ci: r.ci,
        rol_sistema: r.rol_sistema,
        rol_academico: r.rol_academico,
        programas: r.programas
      };
      localStorage.setItem("user", JSON.stringify(payload));
      // actualizar hook (si existe)
      setUser && setUser(payload);
      navigate("/");
    } catch (err) {
      alert(err.message || "Error en login");
    }
  };

  return (
    <div className="login-page">
      <h2>Iniciar sesión</h2>
      <form onSubmit={handleLogin}>
        <input type="email" placeholder="Correo" value={email} onChange={(e)=>setEmail(e.target.value)} />
        <input type="password" placeholder="Contraseña" value={password} onChange={(e)=>setPassword(e.target.value)} />
        <button type="submit">Entrar</button>
      </form>
    </div>
  );
}
