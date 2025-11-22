export const API_URL = "http://localhost:5000/api";

export const api = {
  get: async (endpoint) => {
    const res = await fetch(`${API_URL}${endpoint}`);
    if (!res.ok) {
      let err = new Error("Error en la API");
      try {
        const body = await res.json();
        err.message = body.error || body.message || err.message;
      } catch (e) {
        /* ignore */
      }
      throw err;
    }
    return res.json();
  },

  post: async (endpoint, data) => {
    const res = await fetch(`${API_URL}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      let err = new Error("Error en la API");
      try {
        const body = await res.json();
        err.message = body.error || body.message || err.message;
      } catch (e) {}
      throw err;
    }
    return res.json();
  },

  put: async (endpoint, data) => {
    const res = await fetch(`${API_URL}${endpoint}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Error en la API");
    return res.json();
  },

  del: async (endpoint) => {
    const res = await fetch(`${API_URL}${endpoint}`, { method: "DELETE" });
    if (!res.ok) throw new Error("Error en la API");
    return res.json();
  },
};
