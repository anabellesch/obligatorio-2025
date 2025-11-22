from datetime import datetime, time, timedelta, date
from db import get_conn

def hour_int_from_time_str(tstr):
    # espera "HH:MM" o "H:MM"
    h = int(tstr.split(":")[0])
    m = int(tstr.split(":")[1])
    if m != 0:
        raise ValueError("Los minutos deben ser 00: reservar por bloques de hora exactos")
    return h

def validate_hours_between_8_23(h_start, h_end):
    if h_start < 8 or h_end > 23 or h_end <= h_start:
        raise ValueError("Turnos permitidos entre 08:00 y 23:00 y hora_fin > hora_inicio")

def week_bounds_for_date(d: date):
    # devuelve (start_of_week_date, end_of_week_date) as dates, assuming week starts Monday
    start = d - timedelta(days=d.weekday())
    end = start + timedelta(days=6)
    return start, end

def is_docente(ci):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    # si existe algún registro con rol='docente' para el ci lo consideramos docente
    cur.execute("""
        SELECT 1 FROM participante_programa_academico
         WHERE ci_participante = %s AND rol = 'docente' LIMIT 1
    """, (ci,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    return bool(r)

def is_posgrado(ci):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    # Verificamos si existe participante en un programa cuyo tipo = 'posgrado'
    cur.execute("""
        SELECT 1
        FROM participante_programa_academico ppa
        JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
        WHERE ppa.ci_participante = %s AND pa.tipo = 'posgrado'
        LIMIT 1
    """, (ci,))
    r = cur.fetchone()
    cur.close()
    conn.close()
    return bool(r)
