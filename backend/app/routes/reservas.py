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
    # Return reservation info joined with sala and turno so frontend can show sala name and turno times
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
    # Expecting: { id_sala: int, fecha: 'YYYY-MM-DD', id_turno: int, ci_solicitante: string, participantes: [ci] }
    id_sala = data.get('id_sala')
    fecha = data.get('fecha')  # "YYYY-MM-DD"
    id_turno = data.get('id_turno')
    ci_solicitante = data.get('ci_solicitante')
    participantes = data.get('participantes') or []
    estado = "activa"

    if not id_sala or not fecha or not id_turno:
        return jsonify({'error': 'Faltan parametros id_sala, fecha o id_turno'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Insert reserva
        cursor.execute(
            "INSERT INTO reserva (id_sala, fecha, id_turno, estado) VALUES (%s, %s, %s, %s)",
            (id_sala, fecha, id_turno, estado)
        )
        conn.commit()
        # get inserted id
        cursor.execute("SELECT LAST_INSERT_ID() as id")
        id_res = cursor.fetchone()[0]

        # insert solicitante as participante too if provided
        to_insert = []
        if ci_solicitante:
            to_insert.append(ci_solicitante)
        # add other participants, avoid duplicates
        for ci in participantes:
            if ci not in to_insert:
                to_insert.append(ci)

        for ci in to_insert:
            cursor.execute(
                "INSERT INTO reserva_participante (ci_participante, id_reserva) VALUES (%s, %s)",
                (ci, id_res)
            )
        conn.commit()
        return jsonify({"message": "Reserva creada", "id_reserva": id_res}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
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