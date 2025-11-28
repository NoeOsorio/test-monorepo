import os
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/noe_db')

def get_db_connection():
    """Obtiene una conexión a la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051, debug=True)


