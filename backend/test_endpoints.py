import requests

BASE = "http://localhost:5000/api"

endpoints = [
    "/auth/login",
    "/participantes",
    "/salas",
    "/reservas",
    "/sanciones",
    "/reportes"
]

print("====== TEST API ======")

for ep in endpoints:
    try:
        r = requests.get(BASE + ep)
        print(ep, r.status_code)
    except Exception as e:
        print(ep, "ERROR:", e)

print("======================")
