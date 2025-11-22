from flask import Blueprint, request, jsonify
from app.db import execute_query
from datetime import datetime, timedelta

sanciones_bp = Blueprint('sanciones', __name__)

# GET todas las sanciones
@sanciones_bp.route('/', methods=['GET'])
def get_sanctions():
    """Obtiene todas las sanciones"""
    try:
        ci_participante = request.args.get('ci_participante')
        activas_solo = request.args.get('activas')
        
        query = """
            SELECT s.id_sancion, s.ci_participante, s.fecha_inicio, s.fecha_fin, s.motivo,
                   p.nombre, p.apellido, p.email
            FROM sancion_participante s
            JOIN participante p ON s.ci_participante = p.ci
        """
        
        conditions = []
        params = []
        
        if ci_participante:
            conditions.append("s.ci_participante = %s")
            params.append(ci_participante)
        
        if activas_solo:
            conditions.append("CURDATE() BETWEEN s.fecha_inicio AND s.fecha_fin")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY s.fecha_inicio DESC"
        
        results = execute_query(query, tuple(params) if params else None)
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET sanción específica
@sanciones_bp.route('/<int:id_sancion>', methods=['GET'])
def get_sanction(id_sancion):
    """Obtiene una sanción específica"""
    try:
        query = """
            SELECT s.id_sancion, s.ci_participante, s.fecha_inicio, s.fecha_fin, s.motivo,
                   p.nombre, p.apellido, p.email
            FROM sancion_participante s
            JOIN participante p ON s.ci_participante = p.ci
            WHERE s.id_sancion = %s
        """
        results = execute_query(query, (id_sancion,))
        
        if not results:
            return jsonify({"error": "Sanción no encontrada"}), 404
        
        return jsonify(results[0]), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST crear sanción
@sanciones_bp.route('/', methods=['POST'])
def create_sanction():
    """Crea una nueva sanción"""
    try:
        data = request.json
        
        # Validar campos requeridos
        required = ['ci_participante', 'fecha_inicio', 'fecha_fin']
        if not all(field in data for field in required):
            return jsonify({"error": "Faltan campos requeridos"}), 400
        
        ci_participante = data['ci_participante']
        fecha_inicio = data['fecha_inicio']
        fecha_fin = data['fecha_fin']
        motivo = data.get('motivo', 'Sanción administrativa')
        
        # Validar que el participante existe
        check_query = "SELECT COUNT(*) as count FROM participante WHERE ci = %s"
        result = execute_query(check_query, (ci_participante,))
        
        if result[0]['count'] == 0:
            return jsonify({"error": "El participante no existe"}), 404
        
        # Validar fechas
        fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        
        if fecha_fin_obj <= fecha_inicio_obj:
            return jsonify({"error": "La fecha de fin debe ser posterior a la fecha de inicio"}), 400
        
        # Insertar sanción
        query = """
            INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin, motivo)
            VALUES (%s, %s, %s, %s)
        """
        params = (ci_participante, fecha_inicio, fecha_fin, motivo)
        
        result = execute_query(query, params)
        
        return jsonify({
            "message": "Sanción creada exitosamente",
            "id_sancion": result['last_id']
        }), 201
    
    except ValueError as e:
        return jsonify({"error": "Formato de fecha inválido. Use YYYY-MM-DD"}), 400
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT actualizar sanción
@sanciones_bp.route('/<int:id_sancion>', methods=['PUT'])
def update_sanction(id_sancion):
    """Actualiza una sanción existente"""
    try:
        data = request.json
        
        # Construir query dinámicamente
        updates = []
        params = []
        
        if 'fecha_inicio' in data:
            updates.append("fecha_inicio = %s")
            params.append(data['fecha_inicio'])
        
        if 'fecha_fin' in data:
            updates.append("fecha_fin = %s")
            params.append(data['fecha_fin'])
        
        if 'motivo' in data:
            updates.append("motivo = %s")
            params.append(data['motivo'])
        
        if not updates:
            return jsonify({"error": "No hay campos para actualizar"}), 400
        
        params.append(id_sancion)
        query = f"UPDATE sancion_participante SET {', '.join(updates)} WHERE id_sancion = %s"
        
        result = execute_query(query, tuple(params))
        
        if result['affected_rows'] == 0:
            return jsonify({"error": "Sanción no encontrada"}), 404
        
        return jsonify({"message": "Sanción actualizada exitosamente"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE eliminar sanción
@sanciones_bp.route('/<int:id_sancion>', methods=['DELETE'])
def delete_sanction(id_sancion):
    """Elimina una sanción"""
    try:
        query = "DELETE FROM sancion_participante WHERE id_sancion = %s"
        result = execute_query(query, (id_sancion,))
        
        if result['affected_rows'] == 0:
            return jsonify({"error": "Sanción no encontrada"}), 404
        
        return jsonify({"message": "Sanción eliminada exitosamente"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET verificar si participante tiene sanción activa
@sanciones_bp.route('/verificar/<string:ci>', methods=['GET'])
def check_active_sanction(ci):
    """Verifica si un participante tiene sanción activa"""
    try:
        query = """
            SELECT id_sancion, fecha_inicio, fecha_fin, motivo
            FROM sancion_participante
            WHERE ci_participante = %s 
            AND CURDATE() BETWEEN fecha_inicio AND fecha_fin
            ORDER BY fecha_fin DESC
            LIMIT 1
        """
        results = execute_query(query, (ci,))
        
        if results:
            return jsonify({
                "tiene_sancion": True,
                "sancion": results[0]
            }), 200
        else:
            return jsonify({
                "tiene_sancion": False,
                "sancion": None
            }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500