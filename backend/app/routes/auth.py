from flask import Blueprint, request, jsonify
from app.db import execute_query
import hashlib
import secrets

auth_bp = Blueprint('auth', __name__)

def hash_password(password):
    """Hashea una contraseña usando SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token():
    """Genera un token aleatorio para la sesión"""
    return secrets.token_hex(32)

# POST login
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Autenticar usuario
    Body: { "email": "...", "password": "..." }
    """
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email y contraseña son requeridos"}), 400
        
        # Buscar usuario por email
        query = """
            SELECT l.correo, l.ci_participante, p.nombre, p.apellido, p.email
            FROM login l
            JOIN participante p ON l.ci_participante = p.ci
            WHERE l.correo = %s
        """
        results = execute_query(query, (email,))
        
        if not results:
            return jsonify({"error": "Credenciales inválidas"}), 401
        
        user = results[0]
        

 
        password_hash = hash_password(password)
        
        
        query_pass = "SELECT password_hash FROM login WHERE correo = %s"
        pass_result = execute_query(query_pass, (email,))
        if pass_result[0]['password_hash'] != password_hash:
                return jsonify({"error": "Credenciales inválidas"}), 401
        
        # Generar token de sesión
        token = generate_token()
        
        # Obtener roles del usuario
        query_roles = """
            SELECT ppa.rol, pa.tipo
            FROM participante_programa_academico ppa
            JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
            WHERE ppa.ci_participante = %s
        """
        roles = execute_query(query_roles, (user['ci_participante'],))
        
        return jsonify({
            "message": "Login exitoso",
            "token": token,
            "user": {
                "ci": user['ci_participante'],
                "nombre": user['nombre'],
                "apellido": user['apellido'],
                "email": user['email'],
                "roles": roles
            }
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST register
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registrar nuevo usuario
    Body: { "ci": "...", "nombre": "...", "apellido": "...", "email": "...", "password": "..." }
    """
    try:
        data = request.json
        
        required = ['ci', 'nombre', 'apellido', 'email', 'password']
        if not all(field in data for field in required):
            return jsonify({"error": "Faltan campos requeridos"}), 400
        
        # Verificar si el usuario ya existe
        check_query = """
            SELECT COUNT(*) as count 
            FROM participante 
            WHERE ci = %s OR email = %s
        """
        result = execute_query(check_query, (data['ci'], data['email']))
        
        if result[0]['count'] > 0:
            return jsonify({"error": "El usuario ya existe"}), 409
        
        # Crear participante
        query_participante = """
            INSERT INTO participante (ci, nombre, apellido, email)
            VALUES (%s, %s, %s, %s)
        """
        execute_query(query_participante, (
            data['ci'],
            data['nombre'],
            data['apellido'],
            data['email']
        ))
        
        # Crear login
        password_hash = hash_password(data['password'])
        query_login = """
            INSERT INTO login (correo, password_hash, ci_participante)
            VALUES (%s, %s, %s)
        """
        execute_query(query_login, (data['email'], password_hash, data['ci']))
        
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Cerrar sesión (principalmente para el frontend)"""
    return jsonify({"message": "Sesión cerrada exitosamente"}), 200

# GET verificar token
@auth_bp.route('/verify', methods=['GET'])
def verify():
    """Verifica si un token es válido"""
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({"valid": False, "error": "Token no proporcionado"}), 401

    return jsonify({"valid": True}), 200