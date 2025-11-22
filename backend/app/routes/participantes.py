from flask import Blueprint, request, jsonify
from app.db import execute_query
import mysql.connector

participantes_bp = Blueprint('participantes', __name__)

# GET todos los participantes
@participantes_bp.route('/', methods=['GET'])
def get_participants():
    """Obtiene todos los participantes"""
    try:
        query = "SELECT ci, nombre, apellido, email FROM participante ORDER BY apellido, nombre"
        results = execute_query(query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET participante por CI
@participantes_bp.route('/<string:ci>', methods=['GET'])
def get_participant(ci):
    """Obtiene un participante específico"""
    try:
        query = "SELECT ci, nombre, apellido, email FROM participante WHERE ci = %s"
        results = execute_query(query, (ci,))
        
        if not results:
            return jsonify({"error": "Participante no encontrado"}), 404
        
        return jsonify(results[0]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST crear participante
@participantes_bp.route('/', methods=['POST'])
def create_participant():
    """Crea un nuevo participante"""
    try:
        data = request.json
        
        # Validar campos requeridos
        required = ['ci', 'nombre', 'apellido', 'email']
        if not all(field in data for field in required):
            return jsonify({"error": "Faltan campos requeridos"}), 400
        
        query = """
            INSERT INTO participante (ci, nombre, apellido, email) 
            VALUES (%s, %s, %s, %s)
        """
        params = (data['ci'], data['nombre'], data['apellido'], data['email'])
        
        execute_query(query, params)
        return jsonify({"message": "Participante creado exitosamente"}), 201
    
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            return jsonify({"error": "Ya existe un participante con esa CI o email"}), 409
        return jsonify({"error": str(e)}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT actualizar participante
@participantes_bp.route('/<string:ci>', methods=['PUT'])
def update_participant(ci):
    """Actualiza un participante existente"""
    try:
        data = request.json
        
        # Construir query dinámicamente
        updates = []
        params = []
        
        if 'nombre' in data:
            updates.append("nombre = %s")
            params.append(data['nombre'])
        if 'apellido' in data:
            updates.append("apellido = %s")
            params.append(data['apellido'])
        if 'email' in data:
            updates.append("email = %s")
            params.append(data['email'])
        
        if not updates:
            return jsonify({"error": "No hay campos para actualizar"}), 400
        
        params.append(ci)
        query = f"UPDATE participante SET {', '.join(updates)} WHERE ci = %s"
        
        result = execute_query(query, tuple(params))
        
        if result['affected_rows'] == 0:
            return jsonify({"error": "Participante no encontrado"}), 404
        
        return jsonify({"message": "Participante actualizado exitosamente"}), 200
    
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            return jsonify({"error": "El email ya está en uso"}), 409
        return jsonify({"error": str(e)}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE eliminar participante
@participantes_bp.route('/<string:ci>', methods=['DELETE'])
def delete_participant(ci):
    """Elimina un participante"""
    try:
        # Verificar si tiene reservas asociadas
        check_query = """
            SELECT COUNT(*) as count 
            FROM reserva_participante 
            WHERE ci_participante = %s
        """
        result = execute_query(check_query, (ci,))
        
        if result[0]['count'] > 0:
            return jsonify({
                "error": "No se puede eliminar el participante porque tiene reservas asociadas"
            }), 409
        
        # Verificar si tiene sanciones
        check_sanciones = """
            SELECT COUNT(*) as count 
            FROM sancion_participante 
            WHERE ci_participante = %s
        """
        result = execute_query(check_sanciones, (ci,))
        
        if result[0]['count'] > 0:
            return jsonify({
                "error": "No se puede eliminar el participante porque tiene sanciones asociadas"
            }), 409
        
        # Eliminar de participante_programa_academico primero
        execute_query("DELETE FROM participante_programa_academico WHERE ci_participante = %s", (ci,))
        
        # Eliminar participante
        query = "DELETE FROM participante WHERE ci = %s"
        result = execute_query(query, (ci,))
        
        if result['affected_rows'] == 0:
            return jsonify({"error": "Participante no encontrado"}), 404
        
        return jsonify({"message": "Participante eliminado exitosamente"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500