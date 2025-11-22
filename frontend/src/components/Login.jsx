import { useState } from 'react';
import { loginUser } from '../services/api';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await loginUser(email, password);
      // Guardar el token en el localStorage o en el estado global
      localStorage.setItem('token', data.token);
      window.location.href = '/dashboard';  // Redirigir a dashboard
    } catch (err) {
      setError(err.error || 'Error de autenticación');
    }
  };

  return (
    <div>
      <h2>Iniciar Sesión</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Correo"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <div>{error}</div>}
        <button type="submit">Iniciar sesión</button>
      </form>
    </div>
  );
}

export default Login;
