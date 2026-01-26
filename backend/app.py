import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor, Json
from dotenv import load_dotenv
from urllib.parse import quote_plus
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_database_url():
    """
    Obtiene la URL de la base de datos desde variables de entorno.
    Prioriza DB_URL, si no existe, construye la URL desde variables individuales.
    """
    # Primero intenta usar DB_URL directamente
    db_url = os.getenv('DB_URL')
    if db_url:
        return db_url
    
    # Si no existe DB_URL, construye la URL desde variables individuales
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'postgres')
    db_user = os.getenv('DB_USER', 'postgres')
    db_pass = os.getenv('DB_PASS', 'postgres')
    
    # Escapa la contraseña por si contiene caracteres especiales
    db_pass_escaped = quote_plus(db_pass)
    
    return f"postgresql://{db_user}:{db_pass_escaped}@{db_host}:{db_port}/{db_name}"

# Configuración de la base de datos
DATABASE_URL = get_database_url()

def get_db_connection():
    """Obtiene una conexión a la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def init_calls_table():
    """Crea la tabla CALLS si no existe"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS calls (
                    id SERIAL PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    snapshot JSONB
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Tabla CALLS inicializada correctamente")
        except psycopg2.Error as e:
            print(f"Error creando tabla CALLS: {e}")
            if conn:
                conn.rollback()
                conn.close()

@app.route("/")
def home():
    return jsonify({"message": "Hello from Flask!"})

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/api/data")
def data():
    return jsonify({"message": "Data from Flask!"})

@app.route("/api/db/test")
def test_db():
    """Endpoint para probar la conexión a la base de datos"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT version();")
            version = cur.fetchone()
            cur.close()
            conn.close()
            return jsonify({
                "status": "success",
                "message": "Conexión a PostgreSQL exitosa",
                "version": version['version'] if version else None
            })
        except psycopg2.Error as e:
            return jsonify({
                "status": "error",
                "message": f"Error ejecutando consulta: {str(e)}"
            }), 500
    else:
        return jsonify({
            "status": "error",
            "message": "No se pudo conectar a la base de datos"
        }), 500

@app.route("/api/calls", methods=["POST"])
def save_call():
    """Endpoint POST que guarda un snapshot con fecha en la tabla CALLS"""
    conn = get_db_connection()
    if not conn:
        return jsonify({
            "status": "error",
            "message": "No se pudo conectar a la base de datos"
        }), 500
    
    try:
        # Obtener los datos del body si existen
        snapshot_data = request.get_json() if request.is_json else None
        
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Insertar el registro con la fecha actual
        if snapshot_data:
            cur.execute("""
                INSERT INTO calls (created_at, snapshot)
                VALUES (CURRENT_TIMESTAMP, %s)
                RETURNING id, created_at, snapshot
            """, (Json(snapshot_data),))
        else:
            cur.execute("""
                INSERT INTO calls (created_at)
                VALUES (CURRENT_TIMESTAMP)
                RETURNING id, created_at, snapshot
            """)
        
        new_call = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "status": "success",
            "message": "Snapshot guardado correctamente",
            "data": {
                "id": new_call['id'],
                "created_at": new_call['created_at'].isoformat() if new_call['created_at'] else None,
                "snapshot": new_call['snapshot']
            }
        }), 201
        
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({
            "status": "error",
            "message": f"Error guardando snapshot: {str(e)}"
        }), 500
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({
            "status": "error",
            "message": f"Error inesperado: {str(e)}"
        }), 500

@app.route("/api/calls", methods=["GET"])
def get_calls():
    """Endpoint GET para obtener todos los calls guardados"""
    conn = get_db_connection()
    if not conn:
        return jsonify({
            "status": "error",
            "message": "No se pudo conectar a la base de datos"
        }), 500
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT id, created_at, snapshot
            FROM calls
            ORDER BY created_at DESC
        """)
        calls = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convertir los resultados a formato JSON
        calls_list = []
        for call in calls:
            calls_list.append({
                "id": call['id'],
                "created_at": call['created_at'].isoformat() if call['created_at'] else None,
                "snapshot": call['snapshot']
            })
        
        return jsonify({
            "status": "success",
            "count": len(calls_list),
            "data": calls_list
        }), 200
        
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
            conn.close()
        return jsonify({
            "status": "error",
            "message": f"Error obteniendo calls: {str(e)}"
        }), 500

@app.route("/api/test/environment-variables")
def test_environment_variables():
    """Endpoint para probar las variables de entorno"""
    environment = os.getenv("FLASK_ENV")
    database_url = os.getenv("DB_URL")
    database_host = os.getenv("DB_HOST")
    database_name = os.getenv("DB_NAME")
    database_port = os.getenv("DB_PORT")
    database_user = os.getenv("DB_USER")
    database_pass = os.getenv("DB_PASS")
    test_database_url = os.getenv("TEST_DB_DB_URL")
    test_database_host = os.getenv("TEST_DB_DB_HOST")
    test_database_name = os.getenv("TEST_DB_DB_NAME")
    test_database_port = os.getenv("TEST_DB_DB_PORT")
    test_database_user = os.getenv("TEST_DB_DB_USER")
    test_database_pass = os.getenv("TEST_DB_DB_PASS")

    return jsonify({
        "status": "success",
        "message": "Environment variables test",
        "environment": environment,
        "database_url": database_url,
        "database_host": database_host,
        "database_name": database_name,
        "database_port": database_port,
        "database_user": database_user,
        "database_pass": database_pass,
        "test_database_url": test_database_url,
        "test_database_host": test_database_host,
        "test_database_name": test_database_name,
        "test_database_port": test_database_port,
        "test_database_user": test_database_user,
        "test_database_pass": test_database_pass
    }), 200

# Inicializar la tabla CALLS al iniciar la aplicación
init_calls_table()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051, debug=True)


