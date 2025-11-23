const defaultHost = typeof window !== 'undefined' ? window.location.hostname : 'localhost';
export const API_URL = import.meta.env.VITE_API_URL || `http://${defaultHost}:5000/api`;

function buildUrl(endpoint) {

  const base = API_URL.replace(/\/$/, "");
  let ep = endpoint || "";
  if (ep.startsWith("/api/")) ep = ep.replace(/^\/api/, "");

  if (/^\/[^\/]+$/.test(ep) && !ep.endsWith('/')) {
    ep = ep + '/';
  }
  const url = `${base}${ep}`;

  if (process.env.NODE_ENV !== 'production') {
    try { console.debug(`[api] buildUrl -> ${url}`); } catch (e) {}
  }
  return url;
}

export const api = {
  get: async (endpoint) => {
    const url = buildUrl(endpoint);
    const res = await fetch(url);
    if (!res.ok) {
      let err = new Error("Error en la API");
      try {
        const body = await res.json();
        err.message = body.error || body.message || err.message;
      } catch (e) {

      }
      throw err;
    }
    return res.json();
  },

  post: async (endpoint, data) => {
    const url = buildUrl(endpoint);
    let res;
    try {

      if (process.env.NODE_ENV !== 'production') {
        try { console.debug('[api] POST', url, data); } catch (e) {}
      }
      res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
    } catch (err) {
  
      const message = `Network error connecting to ${url}: ${err.message}`;
      try { console.error('[api] Network error', { url, err }); } catch (e) {}
      throw new Error(message);
    }
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
    const url = buildUrl(endpoint);
    const res = await fetch(url, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Error en la API");
    return res.json();
  },

  del: async (endpoint) => {
    const url = buildUrl(endpoint);
    const res = await fetch(url, { method: "DELETE" });
    if (!res.ok) throw new Error("Error en la API");
    return res.json();
  },

  
};

export const getReporte = async (path) => {
  const res = await fetch(`${API_URL}/reportes/${path}`);
  if (!res.ok) throw new Error("Error al obtener reporte");
  return res.json();
};

