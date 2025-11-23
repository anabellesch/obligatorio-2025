import React, { useEffect, useState } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { API_URL } from '../services/api';

/**
 * ProtectedRoute: checks for a logged user in localStorage and
 * redirects to /login if not present.
 * Usage: <ProtectedRoute><YourComponent/></ProtectedRoute>
 */
export default function ProtectedRoute({ children }) {
  const location = useLocation();
  const [valid, setValid] = useState(null); // null=checking, true=ok, false=not valid

  useEffect(() => {
    const check = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        setValid(false);
        return;
      }
      try {
        const res = await fetch(`${API_URL}/auth/verify`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (!res.ok) {
          setValid(false);
          return;
        }
        const body = await res.json();
        setValid(Boolean(body.valid));
      } catch (e) {
        setValid(false);
      }
    };
    check();
  }, []);

  if (valid === null) return null; // or a spinner
  if (!valid) return <Navigate to="/login" replace state={{ from: location }} />;
  return children;
}
