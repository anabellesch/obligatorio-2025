from flask import Blueprint, request, jsonify
from app.db import execute_query
import hashlib
import secrets
import mysql.connector

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
        
        # Buscar usuario por email en la tabla login
        query = """
            SELECT l.correo, l.ci_participante, l.rol_sistema,
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
        
        # Generar token de sesión
        token = generate_token()
        
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
                "rol_sistema": user['rol_sistema'],  # 'admin' o 'usuario'
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
        "rol_sistema": "usuario" | "admin" (opcional, por defecto "usuario")
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
        rol_sistema = data.get('rol_sistema', 'usuario')  # Por defecto: usuario
        
        # Validar rol_sistema
        if rol_sistema not in ['admin', 'usuario']:
            return jsonify({"error": "Rol inválido. Use 'admin' o 'usuario'"}), 400
        
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
        
        # Crear participante
        query_participante = """
            INSERT INTO participante (ci, nombre, apellido, email)
            VALUES (%s, %s, %s, %s)
        """
        execute_query(query_participante, (ci, nombre, apellido, email))
        
        # Crear login
        password_hash = hash_password(password)
        query_login = """
            INSERT INTO login (correo, password_hash, ci_participante, rol_sistema)
            VALUES (%s, %s, %s, %s)
        """
        execute_query(query_login, (email, password_hash, ci, rol_sistema))
        
        return jsonify({
            "message": "Usuario registrado exitosamente",
            "user": {
                "ci": ci,
                "nombre": nombre,
                "apellido": apellido,
                "email": email,
                "rol_sistema": rol_sistema
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
    token = request.headers.get('Authorization')
    
    if not token:
        return jsonify({"valid": False, "error": "Token no proporcionado"}), 401

    # En un sistema real, verificarías el token contra una base de datos
    # Por ahora, aceptamos cualquier token
    return jsonify({"valid": True}), 200

# GET información del usuario actual
@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """
    Obtiene información del usuario actual basado en el token
    Header: Authorization: Bearer {token}
    """
    try:
        # En un sistema real, extraerías el user_id del token
        # Por ahora, esperamos que el frontend envíe el email en el header
        email = request.headers.get('X-User-Email')
        
        if not email:
            return jsonify({"error": "No autorizado"}), 401
        
        query = """
            SELECT l.correo, l.ci_participante, l.rol_sistema,
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
            "email": user['email'],
            "rol_sistema": user['rol_sistema']
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500