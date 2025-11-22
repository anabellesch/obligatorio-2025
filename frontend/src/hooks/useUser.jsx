import { useEffect, useState } from "react";

export function useUser() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const saved = localStorage.getItem("user");
    if (saved) setUser(JSON.parse(saved));
  }, []);

  const logout = () => {
    localStorage.removeItem("user");
    setUser(null);
    // opcional: redirect
    window.location.href = "/login";
  };

  return { user, setUser, logout };
}
