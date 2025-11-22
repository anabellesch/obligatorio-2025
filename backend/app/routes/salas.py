from flask import Blueprint, request, jsonify
import mysql.connector
import os

salas_bp = Blueprint('salas', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT"))
    )

@salas_bp.route('/', methods=['GET'])
def get_rooms():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT s.id_sala, s.nombre_sala, e.nombre_edificio AS nombre_edificio, s.capacidad, s.tipo_sala "
        "FROM sala s JOIN edificio e ON s.id_edificio = e.id_edificio"
    )
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)


@salas_bp.route('/turnos', methods=['GET'])
def get_turnos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # devolver horas en formato HH:MM:SS (frontend usa substring(0,5))
    cursor.execute("SELECT id_turno, TIME_FORMAT(hora_inicio, '%H:%i:%s') AS hora_inicio, TIME_FORMAT(hora_fin, '%H:%i:%s') AS hora_fin FROM turno ORDER BY hora_inicio")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)


@salas_bp.route('/disponibles', methods=['POST'])
def salas_disponibles():
    data = request.json or {}
    fecha = data.get('fecha')
    id_turno = data.get('id_turno')
    if not fecha or not id_turno:
        return jsonify({'error': 'Faltan parametros fecha o id_turno'}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # salas que no tienen reserva activa para la fecha y turno indicados
    cursor.execute(
        """
        SELECT s.id_sala, s.nombre_sala, s.capacidad, s.tipo_sala,
               e.nombre_edificio AS nombre_edificio, e.direccion
        FROM sala s
        JOIN edificio e ON s.id_edificio = e.id_edificio
        WHERE s.id_sala NOT IN (
            SELECT id_sala FROM reserva WHERE fecha = %s AND id_turno = %s AND estado = 'activa'
        )
        ORDER BY s.nombre_sala
        """,
        (fecha, id_turno)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@salas_bp.route('/', methods=['POST'])
def create_room():
    data = request.json
    nombre_sala = data.get('nombre_sala')
    id_edificio = data.get('id_edificio')
    capacidad = data.get('capacidad')
    tipo_sala = data.get('tipo_sala')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sala (nombre_sala, id_edificio, capacidad, tipo_sala) VALUES (%s, %s, %s, %s)",
        (nombre_sala, id_edificio, capacidad, tipo_sala)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Sala creada"}), 201
