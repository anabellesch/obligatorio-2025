from flask import Blueprint, request, jsonify
from app.db import execute_query, execute_transaction
import hashlib
import os
import mysql.connector
import jwt
import datetime

auth_bp = Blueprint('auth', __name__)

JWT_SECRET = os.getenv('JWT_SECRET', 'dev-jwt-secret')
JWT_ALGORITHM = 'HS256'
JWT_EXP_HOURS = int(os.getenv('JWT_EXP_HOURS', '8'))

def hash_password(password):
    """Hashea una contraseña usando SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_jwt(payload: dict):
    exp = datetime.datetime.utcnow() + datetime.timedelta(hours=JWT_EXP_HOURS)
    payload_copy = payload.copy()
    payload_copy['exp'] = exp
    token = jwt.encode(payload_copy, JWT_SECRET, algorithm=JWT_ALGORITHM)
    # PyJWT returns str in v2
    return token

def verify_jwt(token: str):
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return True, data
    except jwt.ExpiredSignatureError:
        return False, {'error': 'Token expirado'}
    except jwt.InvalidTokenError:
        return False, {'error': 'Token inválido'}

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
        
        # Buscar usuario por email en la tabla login
        query = """
            SELECT l.correo, l.ci_participante,
                   p.nombre, p.apellido, p.email
            FROM login l
            JOIN participante p ON l.ci_participante = p.ci
            WHERE l.correo = %s
        """
        results = execute_query(query, (email,))
        
        if not results:
            return jsonify({"error": "Credenciales inválidas"}), 401
        
        user = results[0]
        
        # Verificar contraseña
        password_hash = hash_password(password)
        
        query_pass = "SELECT password_hash FROM login WHERE correo = %s"
        pass_result = execute_query(query_pass, (email,))
        
        if not pass_result or pass_result[0]['password_hash'] != password_hash:
            return jsonify({"error": "Credenciales inválidas"}), 401
        
        # Generar JWT de sesión (sin rol)
        token = generate_jwt({
            'email': user['email'],
            'ci': user['ci_participante']
        })
        
        # Obtener roles académicos del usuario (si tiene)
        query_roles = """
            SELECT ppa.rol, pa.tipo, pa.nombre_programa
            FROM participante_programa_academico ppa
            JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
            WHERE ppa.ci_participante = %s
        """
        roles_academicos = execute_query(query_roles, (user['ci_participante'],))
        
        return jsonify({
            "message": "Login exitoso",
            "token": token,
            "user": {
                "ci": user['ci_participante'],
                "nombre": user['nombre'],
                "apellido": user['apellido'],
                "email": user['email'],
                "roles_academicos": roles_academicos
            }
        }), 200
    
    except Exception as e:
        print(f"Error en login: {e}")
        return jsonify({"error": str(e)}), 500

# POST register
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registrar nuevo usuario
    Body: { 
        "ci": "...", 
        "nombre": "...", 
        "apellido": "...", 
        "email": "...", 
        "password": "...",
        
    }
    """
    try:
        data = request.json
        
        required = ['ci', 'nombre', 'apellido', 'email', 'password']
        if not all(field in data for field in required):
            return jsonify({"error": "Faltan campos requeridos"}), 400
        
        ci = data['ci']
        nombre = data['nombre']
        apellido = data['apellido']
        email = data['email']
        password = data['password']
        
        
        # Verificar que la contraseña tenga al menos 6 caracteres
        if len(password) < 6:
            return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400
        
        # Verificar si el usuario ya existe (por CI o email)
        check_query = """
            SELECT COUNT(*) as count 
            FROM participante 
            WHERE ci = %s OR email = %s
        """
        result = execute_query(check_query, (ci, email))
        
        if result[0]['count'] > 0:
            return jsonify({"error": "Ya existe un usuario con esa CI o email"}), 409
        
        # Verificar si el correo ya está registrado en login
        check_login = """
            SELECT COUNT(*) as count 
            FROM login 
            WHERE correo = %s
        """
        result_login = execute_query(check_login, (email,))
        
        if result_login[0]['count'] > 0:
            return jsonify({"error": "El email ya está registrado"}), 409
        
        # Crear participante y login en una sola transacción
        query_participante = (
            "INSERT INTO participante (ci, nombre, apellido, email) VALUES (%s, %s, %s, %s)",
            (ci, nombre, apellido, email)
        )

        password_hash = hash_password(password)
        query_login = (
            "INSERT INTO login (correo, password_hash, ci_participante) VALUES (%s, %s, %s)",
            (email, password_hash, ci)
        )

        # Ejecutar ambos inserts en la misma transacción (si falla uno, se hace rollback)
        execute_transaction([query_participante, query_login])
        
        return jsonify({
            "message": "Usuario registrado exitosamente",
            "user": {
                "ci": ci,
                "nombre": nombre,
                "apellido": apellido,
                "email": email
            }
        }), 201
    
    except mysql.connector.IntegrityError as e:
        return jsonify({"error": "Error de integridad en la base de datos"}), 500
    except Exception as e:
        print(f"Error en register: {e}")
        return jsonify({"error": str(e)}), 500

# POST logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Cerrar sesión (principalmente para el frontend)"""
    return jsonify({"message": "Sesión cerrada exitosamente"}), 200

# GET verificar token (para proteger rutas)
@auth_bp.route('/verify', methods=['GET'])
def verify():
    """Verifica si un token es válido"""
    auth = request.headers.get('Authorization')
    if not auth:
        return jsonify({"valid": False, "error": "Token no proporcionado"}), 401

    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return jsonify({"valid": False, "error": "Formato de Authorization inválido"}), 401

    token = parts[1]
    ok, data = verify_jwt(token)
    if not ok:
        return jsonify({"valid": False, "error": data.get('error', 'invalid token')}), 401
    return jsonify({"valid": True, "payload": data}), 200

# GET información del usuario actual
@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """
    Obtiene información del usuario actual basado en el token
    Header: Authorization: Bearer {token}
    """
    try:
        # Ahora verificamos el token Bearer y extraemos el email del payload
        auth = request.headers.get('Authorization')
        if not auth:
            return jsonify({"error": "No autorizado"}), 401
        parts = auth.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({"error": "No autorizado"}), 401
        token = parts[1]
        ok, payload = verify_jwt(token)
        if not ok:
            return jsonify({"error": payload.get('error', 'Token inválido')}), 401
        email = payload.get('email')
        if not email:
            return jsonify({"error": "Email en token ausente"}), 401

        query = """
            SELECT l.correo, l.ci_participante,
                   p.nombre, p.apellido, p.email
            FROM login l
            JOIN participante p ON l.ci_participante = p.ci
            WHERE l.correo = %s
        """
        results = execute_query(query, (email,))
        
        if not results:
            return jsonify({"error": "Usuario no encontrado"}), 404
        
        user = results[0]
        
        return jsonify({
            "ci": user['ci_participante'],
            "nombre": user['nombre'],
            "apellido": user['apellido'],
            "email": user['email']
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500