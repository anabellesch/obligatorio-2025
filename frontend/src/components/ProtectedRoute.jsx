import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';

/**
 * ProtectedRoute: checks for a logged user in localStorage and
 * redirects to /login if not present.
 * Usage: <ProtectedRoute><YourComponent/></ProtectedRoute>
 */
export default function ProtectedRoute({ children }) {
  const location = useLocation();
  try {
    const saved = localStorage.getItem('user');
    if (!saved) {
      return <Navigate to="/login" replace state={{ from: location }} />;
    }
    return children;
  } catch (e) {
    return <Navigate to="/login" replace state={{ from: location }} />;
  }
}
