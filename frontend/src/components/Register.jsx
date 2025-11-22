import { useState } from 'react';
import { registerUser } from '../services/api'; // Asegúrate de tener esta función en `api.js`

function Register() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [ci, setCi] = useState('');
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await registerUser(ci, nombre, apellido, email, password);
      window.location.href = '/login';  // Redirigir al login
    } catch (err) {
      setError(err.error || 'Error de registro');
    }
  };

  return (
    <div>
      <h2>Registrar Usuario</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="CI"
          value={ci}
          onChange={(e) => setCi(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Nombre"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Apellido"
          value={apellido}
          onChange={(e) => setApellido(e.target.value)}
          required
        />
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
        <button type="submit">Registrar</button>
      </form>
    </div>
  );
}

export default Register;
