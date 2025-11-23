import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:5000/api"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name):
    print(f"\n{Colors.BLUE}🧪 TEST: {name}{Colors.END}")

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

# =============================================================================
# TESTS DE PARTICIPANTES
# =============================================================================

def test_crear_participantes():
    print_test("Crear participantes de prueba")
    
    participantes = [
        {"ci": "12345678", "nombre": "Juan", "apellido": "Pérez", "email": "juan@test.com"},
        {"ci": "87654321", "nombre": "María", "apellido": "García", "email": "maria@test.com"},
        {"ci": "11111111", "nombre": "Pedro", "apellido": "López", "email": "pedro@test.com"},
    ]
    
    for p in participantes:
        try:
            res = requests.post(f"{BASE_URL}/participantes/", json=p)
            if res.status_code in [201, 409]:  # 409 = ya existe
                print_success(f"Participante {p['nombre']} {p['apellido']} OK")
            else:
                print_error(f"Error creando {p['nombre']}: {res.text}")
        except Exception as e:
            print_error(f"Error de conexión: {e}")

# =============================================================================
# TESTS DE SALAS
# =============================================================================

def test_listar_salas():
    print_test("Listar salas disponibles")
    
    try:
        res = requests.get(f"{BASE_URL}/salas/")
        if res.status_code == 200:
            salas = res.json()
            print_success(f"Total de salas: {len(salas)}")
            
            # Mostrar algunas salas
            for sala in salas[:3]:
                print(f"  • {sala['nombre_sala']} - Capacidad: {sala['capacidad']} - Tipo: {sala['tipo_sala']}")
        else:
            print_error(f"Error listando salas: {res.text}")
    except Exception as e:
        print_error(f"Error de conexión: {e}")

def test_listar_turnos():
    print_test("Listar turnos disponibles")
    
    try:
        res = requests.get(f"{BASE_URL}/salas/turnos")
        if res.status_code == 200:
            turnos = res.json()
            print_success(f"Total de turnos: {len(turnos)}")
            
            # Mostrar algunos turnos
            for turno in turnos[:3]:
                print(f"  • Turno {turno['id_turno']}: {turno['hora_inicio']} - {turno['hora_fin']}")
        else:
            print_error(f"Error listando turnos: {res.text}")
    except Exception as e:
        print_error(f"Error de conexión: {e}")

# =============================================================================
# TESTS DE RESERVAS - REGLAS DE NEGOCIO
# =============================================================================

def test_reserva_basica():
    print_test("Crear reserva básica")
    
    fecha = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    reserva = {
        "id_sala": 1,
        "fecha": fecha,
        "id_turno": 1,
        "ci_solicitante": "12345678",
        "participantes": ["12345678"]
    }
    
    try:
        res = requests.post(f"{BASE_URL}/reservas/", json=reserva)
        if res.status_code == 201:
            print_success(f"Reserva creada exitosamente")
            data = res.json()
            print(f"  ID de reserva: {data.get('id_reserva')}")
        else:
            print_error(f"Error: {res.text}")
    except Exception as e:
        print_error(f"Error de conexión: {e}")

def test_limite_2_horas_diarias():
    print_test("REGLA: Máximo 2 horas diarias (estudiantes grado)")
    
    fecha = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
    
    # Intentar reservar 3 bloques el mismo día (debe fallar)
    for turno in [2, 3, 4]:
        reserva = {
            "id_sala": 1,
            "fecha": fecha,
            "id_turno": turno,
            "ci_solicitante": "87654321",
            "participantes": ["87654321"]
        }
        
        try:
            res = requests.post(f"{BASE_URL}/reservas/", json=reserva)
            if turno <= 3:
                if res.status_code == 201:
                    print_success(f"Turno {turno} reservado OK")
                else:
                    print_warning(f"Turno {turno}: {res.text}")
            else:
                if res.status_code != 201:
                    print_success(f"❌ Turno {turno} rechazado correctamente (límite 2h)")
                else:
                    print_error(f"⚠️  Se permitió el 3er turno (debería fallar)")
        except Exception as e:
            print_error(f"Error: {e}")

def test_capacidad_sala():
    print_test("REGLA: Capacidad máxima de sala")
    
    fecha = (date.today() + timedelta(days=3)).strftime("%Y-%m-%d")
    
    # Obtener capacidad de sala 1
    try:
        res_salas = requests.get(f"{BASE_URL}/salas/")
        sala = [s for s in res_salas.json() if s['id_sala'] == 1][0]
        capacidad = sala['capacidad']
        
        print(f"Sala 1 tiene capacidad: {capacidad}")
        
        # Intentar reservar con más participantes de lo permitido
        participantes_exceso = ["12345678"] * (capacidad + 2)
        
        reserva = {
            "id_sala": 1,
            "fecha": fecha,
            "id_turno": 5,
            "ci_solicitante": "12345678",
            "participantes": participantes_exceso
        }
        
        res = requests.post(f"{BASE_URL}/reservas/", json=reserva)
        if res.status_code != 201:
            print_success("Reserva rechazada correctamente (exceso de capacidad)")
        else:
            print_error("⚠️  Se permitió exceder la capacidad")
            
    except Exception as e:
        print_error(f"Error: {e}")

def test_salas_disponibles():
    print_test("Verificar disponibilidad de salas")
    
    fecha = (date.today() + timedelta(days=4)).strftime("%Y-%m-%d")
    
    payload = {
        "fecha": fecha,
        "id_turno": 6
    }
    
    try:
        res = requests.post(f"{BASE_URL}/salas/disponibles", json=payload)
        if res.status_code == 200:
            salas = res.json()
            print_success(f"Salas disponibles: {len(salas)}")
            for sala in salas[:3]:
                print(f"  • {sala['nombre_sala']} - {sala['tipo_sala']}")
        else:
            print_error(f"Error: {res.text}")
    except Exception as e:
        print_error(f"Error: {e}")

# =============================================================================
# TESTS DE SANCIONES
# =============================================================================

def test_crear_sancion():
    print_test("Crear sanción (2 meses)")
    
    fecha_inicio = date.today().strftime("%Y-%m-%d")
    fecha_fin = (date.today() + timedelta(days=60)).strftime("%Y-%m-%d")
    
    sancion = {
        "ci_participante": "11111111",
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "motivo": "No asistió a reserva (TEST)"
    }
    
    try:
        res = requests.post(f"{BASE_URL}/sanciones/", json=sancion)
        if res.status_code == 201:
            print_success("Sanción creada exitosamente")
        else:
            print_warning(f"Respuesta: {res.text}")
    except Exception as e:
        print_error(f"Error: {e}")

def test_verificar_sancion():
    print_test("Verificar si participante tiene sanción activa")
    
    try:
        res = requests.get(f"{BASE_URL}/sanciones/verificar/11111111")
        if res.status_code == 200:
            data = res.json()
            if data['tiene_sancion']:
                print_success(f"✅ Sanción detectada: {data['sancion']['motivo']}")
            else:
                print_warning("No tiene sanciones activas")
        else:
            print_error(f"Error: {res.text}")
    except Exception as e:
        print_error(f"Error: {e}")

# =============================================================================
# TESTS DE REPORTES
# =============================================================================

def test_reportes():
    print_test("Generar reportes del sistema")
    
    reportes = [
        ("Salas más reservadas", "/reportes/salas-mas-reservadas"),
        ("Turnos más demandados", "/reportes/turnos-mas-demandados"),
        ("Promedio participantes", "/reportes/promedio-participantes"),
        ("Estadísticas generales", "/reportes/estadisticas"),
    ]
    
    for nombre, endpoint in reportes:
        try:
            res = requests.get(f"{BASE_URL}{endpoint}")
            if res.status_code == 200:
                print_success(f"✅ {nombre}")
                # Mostrar primeros resultados
                data = res.json()
                if isinstance(data, list) and len(data) > 0:
                    print(f"    Primer resultado: {json.dumps(data[0], indent=2, ensure_ascii=False)}")
                elif isinstance(data, dict):
                    print(f"    {json.dumps(data, indent=2, ensure_ascii=False)}")
            else:
                print_error(f"Error en {nombre}: {res.text}")
        except Exception as e:
            print_error(f"Error: {e}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  TEST DE REGLAS DE NEGOCIO - Sistema Gestión de Salas")
    print(f"{'='*60}{Colors.END}\n")
    
    # 1. Setup inicial
    print(f"\n{Colors.YELLOW}📋 FASE 1: SETUP INICIAL{Colors.END}")
    test_crear_participantes()
    test_listar_salas()
    test_listar_turnos()
    
    # 2. Tests de reservas
    print(f"\n{Colors.YELLOW}📋 FASE 2: TESTS DE RESERVAS{Colors.END}")
    test_reserva_basica()
    test_limite_2_horas_diarias()
    test_capacidad_sala()
    test_salas_disponibles()
    
    # 3. Tests de sanciones
    print(f"\n{Colors.YELLOW}📋 FASE 3: TESTS DE SANCIONES{Colors.END}")
    test_crear_sancion()
    test_verificar_sancion()
    
    # 4. Tests de reportes
    print(f"\n{Colors.YELLOW}📋 FASE 4: TESTS DE REPORTES{Colors.END}")
    test_reportes()
    
    print(f"\n{Colors.GREEN}{'='*60}")
    print(f"  ✅ TESTING COMPLETADO")
    print(f"{'='*60}{Colors.END}\n")

if __name__ == "__main__":
    main()