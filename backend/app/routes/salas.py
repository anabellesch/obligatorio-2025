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
    cursor.execute("SELECT * FROM sala")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@salas_bp.route('/', methods=['POST'])
def create_room():
    data = request.json
    nombre_sala = data.get('nombre_sala')
    edificio = data.get('edificio')
    capacidad = data.get('capacidad')
    tipo_sala = data.get('tipo_sala')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO sala (nombre_sala, edificio, capacidad, tipo_sala) VALUES (%s, %s, %s, %s)",
        (nombre_sala, edificio, capacidad, tipo_sala)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Sala creada"}), 201
