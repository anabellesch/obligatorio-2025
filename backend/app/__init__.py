from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JSON_AS_ASCII'] = False

    # Allow routes to be accessed with or without a trailing slash
    # This prevents Flask from issuing redirects (which break CORS preflight requests)
    app.url_map.strict_slashes = False

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Import and register blueprints (use absolute backend.app.routes imports)
    try:
        from app.routes.auth import auth_bp
        from app.routes.participantes import participantes_bp
        from app.routes.salas import salas_bp
        from app.routes.reservas import reservas_bp
        from app.routes.sanciones import sanciones_bp
        from app.routes.reportes import reportes_bp
        # from app.routes.health import health as health_bp
        
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(participantes_bp, url_prefix='/api/participantes')
        app.register_blueprint(salas_bp, url_prefix='/api/salas')
        app.register_blueprint(reservas_bp, url_prefix='/api/reservas')
        app.register_blueprint(sanciones_bp, url_prefix='/api/sanciones')
        app.register_blueprint(reportes_bp, url_prefix='/api/reportes')
        # app.register_blueprint(health_bp, url_prefix='/api')
        print("Blueprints registrados correctamente.")
    except Exception as e:
        print("ERROR importando blueprints:", e)

    # Test DB connection (non-fatal)
    try:
        from app.db import get_conn
        conn = get_conn()
        conn.close()
        print("Conexión inicial a BD OK")
    except Exception as e:
        print("Atención: No se pudo conectar a BD:", e)

    return app
