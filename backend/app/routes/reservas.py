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
    cursor.execute("SELECT * FROM reserva")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@reservas_bp.route('/', methods=['POST'])
def create_reservation():
    data = request.json
    nombre_sala = data.get('nombre_sala')
    edificio = data.get('edificio')
    fecha = data.get('fecha')  # "YYYY-MM-DD"
    id_turno = data.get('id_turno')
    estado = "activa"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado) VALUES (%s, %s, %s, %s, %s)",
        (nombre_sala, edificio, fecha, id_turno, estado)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Reserva creada"}), 201