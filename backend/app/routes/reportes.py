from flask import Blueprint, request, jsonify
from app.db import execute_query

reportes_bp = Blueprint('reportes', __name__)

# GET salas más reservadas
@reportes_bp.route('/salas-mas-reservadas', methods=['GET'])
def salas_mas_reservadas():
    """
    Retorna las salas más reservadas usando la vista v_salas_mas_reservadas
    """
    query = """
        SELECT id_sala, nombre_sala, nombre_edificio, total_reservas
        FROM v_salas_mas_reservadas
        LIMIT 10
    """
    results = execute_query(query)
    return jsonify(results)

# GET turnos más demandados
@reportes_bp.route('/turnos-mas-demandados', methods=['GET'])
def turnos_mas_demandados():
    """
    Retorna los turnos más demandados usando la vista v_turnos_mas_demandados
    """
    query = """
        SELECT id_turno, hora_inicio, hora_fin, total
        FROM v_turnos_mas_demandados
        LIMIT 10
    """
    results = execute_query(query)
    return jsonify(results)

# GET promedio de participantes por sala
@reportes_bp.route('/promedio-participantes', methods=['GET'])
def promedio_participantes():
    """
    Retorna el promedio de participantes por sala usando la vista
    """
    query = """
        SELECT id_sala, nombre_sala, promedio_participantes
        FROM v_promedio_participantes_por_sala
        ORDER BY promedio_participantes DESC
    """
    results = execute_query(query)
    return jsonify(results)

# GET estadísticas generales
@reportes_bp.route('/estadisticas', methods=['GET'])
def estadisticas_generales():
    """
    Retorna estadísticas generales del sistema
    """
    # Total de reservas
    total_reservas = execute_query("SELECT COUNT(*) as total FROM reserva")[0]['total']
    
    # Reservas activas
    reservas_activas = execute_query(
        "SELECT COUNT(*) as total FROM reserva WHERE estado = 'activa'"
    )[0]['total']
    
    # Total de participantes
    total_participantes = execute_query("SELECT COUNT(*) as total FROM participante")[0]['total']
    
    # Total de salas
    total_salas = execute_query("SELECT COUNT(*) as total FROM sala")[0]['total']
    
    # Participantes sancionados (activos)
    sancionados = execute_query("""
        SELECT COUNT(DISTINCT ci_participante) as total
        FROM sancion_participante
        WHERE CURDATE() BETWEEN fecha_inicio AND fecha_fin
    """)[0]['total']
    
    # Tasa de no asistencia
    sin_asistencia = execute_query(
        "SELECT COUNT(*) as total FROM reserva WHERE estado = 'sin asistencia'"
    )[0]['total']
    
    tasa_no_asistencia = (sin_asistencia / total_reservas * 100) if total_reservas > 0 else 0
    
    return jsonify({
        "total_reservas": total_reservas,
        "reservas_activas": reservas_activas,
        "total_participantes": total_participantes,
        "total_salas": total_salas,
        "participantes_sancionados": sancionados,
        "reservas_sin_asistencia": sin_asistencia,
        "tasa_no_asistencia": round(tasa_no_asistencia, 2)
    })

# GET reservas por rango de fechas
@reportes_bp.route('/reservas-por-fecha', methods=['GET'])
def reservas_por_fecha():
    """
    Retorna un conteo de reservas agrupadas por fecha
    Parámetros opcionales: fecha_inicio, fecha_fin
    """
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    query = """
        SELECT fecha, COUNT(*) as total_reservas,
               SUM(CASE WHEN estado = 'activa' THEN 1 ELSE 0 END) as activas,
               SUM(CASE WHEN estado = 'cancelada' THEN 1 ELSE 0 END) as canceladas,
               SUM(CASE WHEN estado = 'sin asistencia' THEN 1 ELSE 0 END) as sin_asistencia
        FROM reserva
        WHERE 1=1
    """
    params = []
    
    if fecha_inicio:
        query += " AND fecha >= %s"
        params.append(fecha_inicio)
    if fecha_fin:
        query += " AND fecha <= %s"
        params.append(fecha_fin)
    
    query += " GROUP BY fecha ORDER BY fecha DESC"
    
    results = execute_query(query, tuple(params) if params else None)
    return jsonify(results)

# GET uso de salas por tipo
@reportes_bp.route('/uso-por-tipo-sala', methods=['GET'])
def uso_por_tipo_sala():
    """
    Retorna el uso de salas agrupado por tipo (libre, posgrado, docente)
    """
    query = """
        SELECT s.tipo_sala, COUNT(r.id_reserva) as total_reservas,
               COUNT(DISTINCT r.id_sala) as salas_utilizadas
        FROM sala s
        LEFT JOIN reserva r ON s.id_sala = r.id_sala
        GROUP BY s.tipo_sala
    """
    results = execute_query(query)
    return jsonify(results)

# GET participantes más activos
@reportes_bp.route('/participantes-mas-activos', methods=['GET'])
def participantes_mas_activos():
    """
    Retorna los participantes con más reservas
    """
    query = """
        SELECT p.ci, p.nombre, p.apellido, COUNT(rp.id_reserva) as total_reservas,
               SUM(CASE WHEN r.estado = 'activa' THEN 1 ELSE 0 END) as reservas_activas,
               SUM(rp.asistencia) as total_asistencias
        FROM participante p
        JOIN reserva_participante rp ON p.ci = rp.ci_participante
        JOIN reserva r ON rp.id_reserva = r.id_reserva
        GROUP BY p.ci
        ORDER BY total_reservas DESC
        LIMIT 10
    """
    results = execute_query(query)
    return jsonify(results)

# ============== REPORTES REQUERIDOS POR EL OBLIGATORIO ==============

# GET cantidad de reservas por carrera y facultad
@reportes_bp.route('/reservas-por-carrera', methods=['GET'])
def reservas_por_carrera():
    """
    Retorna cantidad de reservas agrupadas por programa académico y facultad
    """
    query = """
        SELECT f.nombre as facultad, 
               pa.nombre_programa as programa,
               pa.tipo as tipo_programa,
               COUNT(DISTINCT r.id_reserva) as total_reservas
        FROM facultad f
        JOIN programa_academico pa ON f.id_facultad = pa.id_facultad
        JOIN participante_programa_academico ppa ON pa.id_programa = ppa.id_programa
        JOIN reserva_participante rp ON ppa.ci_participante = rp.ci_participante
        JOIN reserva r ON rp.id_reserva = r.id_reserva
        GROUP BY f.id_facultad, pa.id_programa
        ORDER BY total_reservas DESC
    """
    results = execute_query(query)
    return jsonify(results)

# GET porcentaje de ocupación de salas por edificio
@reportes_bp.route('/ocupacion-por-edificio', methods=['GET'])
def ocupacion_por_edificio():
    """
    Calcula el porcentaje de ocupación de salas por edificio.
    Considera: (reservas realizadas / espacios disponibles) * 100
    """
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    # Si no se especifican fechas, usar los últimos 30 días
    query = """
        SELECT 
            e.nombre_edificio,
            COUNT(DISTINCT s.id_sala) as total_salas,
            COUNT(DISTINCT r.id_reserva) as total_reservas,
            COUNT(DISTINCT CONCAT(s.id_sala, '-', r.fecha, '-', r.id_turno)) as bloques_ocupados,
            (COUNT(DISTINCT s.id_sala) * 14 * 
                DATEDIFF(
                    COALESCE(%s, CURDATE()), 
                    COALESCE(%s, DATE_SUB(CURDATE(), INTERVAL 30 DAY))
                )
            ) as bloques_totales_disponibles,
            ROUND(
                (COUNT(DISTINCT CONCAT(s.id_sala, '-', r.fecha, '-', r.id_turno)) / 
                 (COUNT(DISTINCT s.id_sala) * 14 * 
                    DATEDIFF(
                        COALESCE(%s, CURDATE()), 
                        COALESCE(%s, DATE_SUB(CURDATE(), INTERVAL 30 DAY))
                    )
                 )
                ) * 100, 2
            ) as porcentaje_ocupacion
        FROM edificio e
        JOIN sala s ON e.id_edificio = s.id_edificio
        LEFT JOIN reserva r ON s.id_sala = r.id_sala
            AND r.fecha BETWEEN COALESCE(%s, DATE_SUB(CURDATE(), INTERVAL 30 DAY)) 
                            AND COALESCE(%s, CURDATE())
        GROUP BY e.id_edificio
        ORDER BY porcentaje_ocupacion DESC
    """
    
    params = (fecha_fin, fecha_inicio, fecha_fin, fecha_inicio, fecha_inicio, fecha_fin)
    results = execute_query(query, params)
    return jsonify(results)

# GET reservas y asistencias por tipo de participante
@reportes_bp.route('/reservas-por-tipo-participante', methods=['GET'])
def reservas_por_tipo_participante():
    """
    Cantidad de reservas y asistencias separadas por profesores, 
    alumnos de grado y alumnos de posgrado
    """
    query = """
        SELECT 
            ppa.rol,
            pa.tipo as tipo_programa,
            COUNT(DISTINCT rp.id_reserva) as total_reservas,
            SUM(rp.asistencia) as total_asistencias,
            ROUND(SUM(rp.asistencia) / COUNT(DISTINCT rp.id_reserva) * 100, 2) as porcentaje_asistencia
        FROM participante_programa_academico ppa
        JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
        JOIN reserva_participante rp ON ppa.ci_participante = rp.ci_participante
        GROUP BY ppa.rol, pa.tipo
        ORDER BY total_reservas DESC
    """
    results = execute_query(query)
    return jsonify(results)

# GET sanciones por tipo de participante
@reportes_bp.route('/sanciones-por-tipo-participante', methods=['GET'])
def sanciones_por_tipo_participante():
    """
    Cantidad de sanciones separadas por profesores, alumnos de grado y posgrado
    """
    query = """
        SELECT 
            ppa.rol,
            pa.tipo as tipo_programa,
            COUNT(sp.id_sancion) as total_sanciones,
            COUNT(DISTINCT sp.ci_participante) as participantes_sancionados,
            SUM(CASE 
                WHEN CURDATE() BETWEEN sp.fecha_inicio AND sp.fecha_fin 
                THEN 1 ELSE 0 
            END) as sanciones_activas
        FROM participante_programa_academico ppa
        JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
        LEFT JOIN sancion_participante sp ON ppa.ci_participante = sp.ci_participante
        GROUP BY ppa.rol, pa.tipo
        ORDER BY total_sanciones DESC
    """
    results = execute_query(query)
    return jsonify(results)

# GET porcentaje de reservas utilizadas vs canceladas
@reportes_bp.route('/efectividad-reservas', methods=['GET'])
def efectividad_reservas():
    """
    Calcula el porcentaje de reservas efectivamente utilizadas vs 
    canceladas o sin asistencia
    """
    query = """
        SELECT 
            COUNT(*) as total_reservas,
            SUM(CASE WHEN estado = 'finalizada' THEN 1 ELSE 0 END) as utilizadas,
            SUM(CASE WHEN estado = 'cancelada' THEN 1 ELSE 0 END) as canceladas,
            SUM(CASE WHEN estado = 'sin asistencia' THEN 1 ELSE 0 END) as sin_asistencia,
            SUM(CASE WHEN estado = 'activa' THEN 1 ELSE 0 END) as activas,
            ROUND(SUM(CASE WHEN estado = 'finalizada' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) 
                as porcentaje_utilizadas,
            ROUND(SUM(CASE WHEN estado = 'cancelada' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) 
                as porcentaje_canceladas,
            ROUND(SUM(CASE WHEN estado = 'sin asistencia' THEN 1 ELSE 0 END) / COUNT(*) * 100, 2) 
                as porcentaje_sin_asistencia
        FROM reserva
    """
    results = execute_query(query)
    return jsonify(results[0] if results else {})

# ============== 3 CONSULTAS ADICIONALES PROPIAS ==============

# GET ranking de edificios por demanda
@reportes_bp.route('/ranking-edificios', methods=['GET'])
def ranking_edificios():
    """
    Ranking de edificios según cantidad de reservas y tasa de ocupación
    """
    query = """
        SELECT 
            e.nombre_edificio,
            e.direccion,
            COUNT(DISTINCT s.id_sala) as total_salas,
            COUNT(r.id_reserva) as total_reservas,
            AVG(s.capacidad) as capacidad_promedio,
            ROUND(COUNT(r.id_reserva) / COUNT(DISTINCT s.id_sala), 2) as reservas_por_sala
        FROM edificio e
        JOIN sala s ON e.id_edificio = s.id_edificio
        LEFT JOIN reserva r ON s.id_sala = r.id_sala
        GROUP BY e.id_edificio
        ORDER BY reservas_por_sala DESC
    """
    results = execute_query(query)
    return jsonify(results)

# GET análisis de horarios pico
@reportes_bp.route('/horarios-pico', methods=['GET'])
def horarios_pico():
    """
    Identifica los horarios con mayor demanda por día de la semana
    """
    query = """
        SELECT 
            DAYNAME(r.fecha) as dia_semana,
            t.hora_inicio,
            t.hora_fin,
            COUNT(*) as total_reservas,
            COUNT(DISTINCT r.id_sala) as salas_diferentes
        FROM reserva r
        JOIN turno t ON r.id_turno = t.id_turno
        WHERE r.estado IN ('activa', 'finalizada')
        GROUP BY DAYOFWEEK(r.fecha), t.id_turno
        ORDER BY total_reservas DESC
        LIMIT 20
    """
    results = execute_query(query)
    return jsonify(results)

# GET predicción de disponibilidad
@reportes_bp.route('/prediccion-disponibilidad', methods=['GET'])
def prediccion_disponibilidad():
    """
    Analiza patrones históricos para predecir disponibilidad futura.
    Muestra qué salas tienen mayor probabilidad de estar disponibles por turno.
    """
    dia_semana = request.args.get('dia_semana', 'Monday')  # Lunes por defecto
    
    query = """
        SELECT 
            s.nombre_sala,
            e.nombre_edificio,
            t.hora_inicio,
            t.hora_fin,
            COUNT(*) as veces_reservada_historico,
            ROUND((1 - COUNT(*) / (
                SELECT COUNT(DISTINCT fecha) 
                FROM reserva 
                WHERE DAYNAME(fecha) = %s
            )) * 100, 2) as probabilidad_disponibilidad
        FROM sala s
        JOIN edificio e ON s.id_edificio = e.id_edificio
        CROSS JOIN turno t
        LEFT JOIN reserva r ON s.id_sala = r.id_sala 
            AND t.id_turno = r.id_turno 
            AND DAYNAME(r.fecha) = %s
        GROUP BY s.id_sala, t.id_turno
        ORDER BY probabilidad_disponibilidad DESC, t.hora_inicio
        LIMIT 30
    """
    results = execute_query(query, (dia_semana, dia_semana))
    return jsonify(results)