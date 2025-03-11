from flask import Flask, jsonify, request
import sqlite3
import os
import logging
from werkzeug.middleware.proxy_fix import ProxyFix
from functools import wraps

# Configuración de la aplicación
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Variables de entorno para configuración
DB_PATH = os.environ.get('DB_PATH', 'volvo.db')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
API_KEY = os.environ.get('API_KEY', 'dev-key')

# Sistema de autenticación básico
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # En producción, usa un sistema más robusto de autenticación
        provided_key = request.headers.get('X-API-Key')
        if provided_key and provided_key == API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized access"}), 401
    return decorated_function

# Conexión a base de datos con manejo de contexto
def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
        return conn
    except sqlite3.Error as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        if conn:
            conn.close()
        return None

# Ruta principal (index)
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "API Volvo funcionando",
        "endpoints_disponibles": {
            "principal": "/api/v1/datos",
            "salud": "/health",
            "tablas": "/tablas",
            "prueba_db": "/test"
        }
    })

# Manejo de errores
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Recurso no encontrado"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Error interno del servidor"}), 500

# Endpoint de verificación de salud para AWS
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

# Endpoint para listar tablas disponibles
@app.route('/tablas', methods=['GET'])
def listar_tablas():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
        
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = [row['name'] for row in cur.fetchall()]
            
            # Adicionalmente, obtener información de cada tabla
            info_tablas = {}
            for tabla in tablas:
                try:
                    cur.execute(f"PRAGMA table_info({tabla})")
                    columnas = [{"nombre": col['name'], "tipo": col['type']} for col in cur.fetchall()]
                    info_tablas[tabla] = columnas
                except:
                    info_tablas[tabla] = "Error al obtener estructura"
            
            return jsonify({
                "tablas_disponibles": tablas,
                "estructura_tablas": info_tablas
            })
    except Exception as e:
        logger.error(f"Error al listar tablas: {e}")
        return jsonify({"error": str(e)}), 500

# Endpoint de prueba simplificado para verificar conexión a DB
@app.route('/test', methods=['GET'])
def test_db():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = [row[0] for row in cursor.fetchall()]
        
        # Intenta contar registros en la tabla "aquiEstoy" si existe
        tabla_info = {}
        if "aquiEstoy" in tablas:
            cursor.execute("SELECT COUNT(*) FROM aquiEstoy")
            count = cursor.fetchone()[0]
            tabla_info["aquiEstoy"] = {"registros": count}
            
            # Obtener una muestra de datos
            cursor.execute("SELECT * FROM aquiEstoy LIMIT 3")
            columnas = [description[0] for description in cursor.description]
            datos = cursor.fetchall()
            muestra = [dict(zip(columnas, fila)) for fila in datos]
            tabla_info["aquiEstoy"]["muestra"] = muestra
        
        conn.close()
        return jsonify({
            "conexion": "exitosa", 
            "base_datos": DB_PATH,
            "tablas_disponibles": tablas,
            "info_tablas": tabla_info
        })
    except Exception as e:
        logger.error(f"Error en prueba de DB: {e}")
        return jsonify({"error": str(e)}), 500

# Endpoint principal para datos
@app.route('/api/v1/datos', methods=['GET'])
# @require_api_key  # Comentado temporalmente para pruebas
def obtener_datos():
    try:
        logger.info("Accediendo al endpoint /api/v1/datos")
        # Parámetros de paginación
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 100, type=int)
        offset = (page - 1) * per_page
        
        conn = get_db_connection()
        if not conn:
            logger.error("No se pudo conectar a la base de datos")
            return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
        
        logger.info(f"Conexión a la base de datos establecida: {DB_PATH}")
        
        # Verificar si la tabla existe
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='aquiEstoy'")
            if not cur.fetchone():
                logger.error("La tabla 'aquiEstoy' no existe")
                return jsonify({"error": "La tabla 'aquiEstoy' no existe en la base de datos"}), 404
            
            logger.info("Tabla 'aquiEstoy' encontrada, ejecutando consulta")
            
            # Consulta paginada
            try:
                query = "SELECT * FROM aquiEstoy LIMIT ? OFFSET ?"
                cur.execute(query, (per_page, offset))
                rows = cur.fetchall()
                
                # Obtener el total de registros para la paginación
                cur.execute("SELECT COUNT(*) FROM aquiEstoy")
                total = cur.fetchone()[0]
                
                # Convertir a lista de diccionarios
                data = [dict(row) for row in rows]
                
                # Información de paginación
                result = {
                    "data": data,
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": total,
                        "pages": (total + per_page - 1) // per_page
                    }
                }
                
                return jsonify(result)
            except sqlite3.Error as e:
                logger.error(f"Error al ejecutar consulta: {e}")
                return jsonify({"error": f"Error al ejecutar consulta: {e}"}), 500
    
    except Exception as e:
        logger.error(f"Error al obtener datos: {e}")
        return jsonify({"error": str(e)}), 500

# Punto de entrada para la aplicación
if __name__ == '__main__':
    logger.info(f"Iniciando aplicación con base de datos: {DB_PATH}")
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)