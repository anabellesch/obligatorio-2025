from flask import Blueprint, request, jsonify
import mysql.connector
import os
from datetime import datetime

reservas_bp = Blueprint('reservas', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )

@reservas_bp.route('/', methods=['GET'])
def get_reservations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT r.id_reserva, r.id_sala, s.nombre_sala, r.id_turno, "
        "TIME_FORMAT(t.hora_inicio, '%H:%i:%s') AS hora_inicio, TIME_FORMAT(t.hora_fin, '%H:%i:%s') AS hora_fin, "
        "r.estado, DATE_FORMAT(r.fecha, '%Y-%m-%d') AS fecha, "
        "DATE_FORMAT(r.fecha_solicitud, '%Y-%m-%d %H:%i:%s') AS fecha_solicitud "
        "FROM reserva r "
        "JOIN sala s ON r.id_sala = s.id_sala "
        "JOIN turno t ON r.id_turno = t.id_turno"
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@reservas_bp.route('/', methods=['POST'])
def create_reservation():
    data = request.json
    id_sala = data.get('id_sala')
    fecha = data.get('fecha')
    id_turno = data.get('id_turno')
    ci_solicitante = data.get('ci_solicitante')
    participantes = data.get('participantes') or []
    estado = "activa"

    if not id_sala or not fecha or not id_turno:
        return jsonify({'error': 'Faltan parametros id_sala, fecha o id_turno'}), 400

    # Si no hay lista de participantes, usar solo el solicitante
    if not participantes and ci_solicitante:
        participantes = [ci_solicitante]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # 1. VERIFICAR CAPACIDAD DE LA SALA
        cursor.execute("SELECT capacidad, tipo_sala FROM sala WHERE id_sala = %s", (id_sala,))
        sala = cursor.fetchone()
        
        if not sala:
            return jsonify({'error': 'Sala no encontrada'}), 404
        
        if len(participantes) > sala['capacidad']:
            return jsonify({
                'error': f'La cantidad de participantes ({len(participantes)}) excede la capacidad de la sala ({sala["capacidad"]})'
            }), 400
        
        # 2. VERIFICAR LÍMITE DE 2 HORAS DIARIAS POR PARTICIPANTE (solo para salas libres)
        # Solo aplica a estudiantes de grado en salas libres
        if sala['tipo_sala'] == 'libre':
            for ci in participantes:
                # Contar cuántas reservas tiene este participante para esta fecha
                cursor.execute("""
                    SELECT COUNT(*) as total
                    FROM reserva_participante rp
                    JOIN reserva r ON rp.id_reserva = r.id_reserva
                    JOIN sala s ON r.id_sala = s.id_sala
                    WHERE rp.ci_participante = %s 
                    AND r.fecha = %s 
                    AND r.estado = 'activa'
                    AND s.tipo_sala = 'libre'
                """, (ci, fecha))
                
                result = cursor.fetchone()
                if result and result['total'] >= 2:
                    return jsonify({
                        'error': f'El participante {ci} ya tiene 2 reservas (2 horas) para esta fecha. Límite alcanzado.'
                    }), 400
        
        # 3. VERIFICAR QUE LA SALA ESTÉ DISPONIBLE
        cursor.execute("""
            SELECT 1 FROM reserva 
            WHERE id_sala = %s AND fecha = %s AND id_turno = %s AND estado = 'activa' 
            LIMIT 1
        """, (id_sala, fecha, id_turno))
        
        if cursor.fetchone():
            return jsonify({'error': 'La sala ya está reservada para ese horario'}), 409
        
        # 4. VERIFICAR QUE NINGÚN PARTICIPANTE TENGA SANCIÓN ACTIVA
        for ci in participantes:
            cursor.execute("""
                SELECT 1 FROM sancion_participante
                WHERE ci_participante = %s 
                AND CURDATE() BETWEEN fecha_inicio AND fecha_fin
                LIMIT 1
            """, (ci,))
            
            if cursor.fetchone():
                return jsonify({
                    'error': f'El participante {ci} tiene una sanción activa y no puede participar en reservas'
                }), 400
        
        # 5. VERIFICAR LÍMITE DE 3 RESERVAS ACTIVAS EN LA SEMANA (solo salas libres)
        if sala['tipo_sala'] == 'libre':
            for ci in participantes:
                cursor.execute("""
                    SELECT COUNT(DISTINCT r.id_reserva) as total
                    FROM reserva_participante rp
                    JOIN reserva r ON rp.id_reserva = r.id_reserva
                    JOIN sala s ON r.id_sala = s.id_sala
                    WHERE rp.ci_participante = %s
                    AND WEEK(r.fecha, 1) = WEEK(%s, 1)
                    AND YEAR(r.fecha) = YEAR(%s)
                    AND r.estado = 'activa'
                    AND s.tipo_sala = 'libre'
                """, (ci, fecha, fecha))
                
                result = cursor.fetchone()
                if result and result['total'] >= 3:
                    return jsonify({
                        'error': f'El participante {ci} ya tiene 3 reservas activas en esta semana. Límite alcanzado.'
                    }), 400
        
        # 6. CREAR LA RESERVA
        cursor.execute("""
            INSERT INTO reserva (id_sala, fecha, id_turno, estado) 
            VALUES (%s, %s, %s, %s)
        """, (id_sala, fecha, id_turno, estado))
        conn.commit()
        
        id_reserva = cursor.lastrowid
        
        # 7. AGREGAR PARTICIPANTES
        for ci in participantes:
            cursor.execute("""
                INSERT INTO reserva_participante (ci_participante, id_reserva) 
                VALUES (%s, %s)
            """, (ci, id_reserva))
        
        conn.commit()
        
        return jsonify({
            "message": "Reserva creada exitosamente",
            "id_reserva": id_reserva
        }), 201
        
    except mysql.connector.Error as err:
        conn.rollback()
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        conn.close()


@reservas_bp.route('/<int:id_reserva>', methods=['DELETE'])
def delete_reservation(id_reserva):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Mark reservation as cancelled
        cursor.execute("UPDATE reserva SET estado = 'cancelada' WHERE id_reserva = %s", (id_reserva,))
        if cursor.rowcount == 0:
            conn.commit()
            return jsonify({'error': 'Reserva no encontrada'}), 404
        conn.commit()
        return jsonify({'message': 'Reserva cancelada'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()