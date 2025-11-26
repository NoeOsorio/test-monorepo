from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Hello from Flask!"})

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy"})

@app.route("/api/data")
def data():
    return jsonify({"message": "Data from Flask!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5051, debug=True)


