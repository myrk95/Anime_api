from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from connection import Connection

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({"success": False, "mensaje": "Funcionalidad login no implementada aún"}), 501

@app.route('/registro', methods=['POST', 'OPTIONS'])
def registro():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json()
    nombre = data.get('nombre')
    apellidos = data.get('apellidos')
    email = data.get('email')  # frontend envia 'email'
    password = data.get('password')
    rol = data.get('rol')

    if not all([nombre, apellidos, email, password, rol]):
        return jsonify({"success": False, "mensaje": "Faltan datos"}), 400

    db = Connection()
    conn = db.conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, apellidos, mail, password, rol) VALUES (%s, %s, %s, %s, %s)",
            (nombre, apellidos, email, password, rol)
        )
        conn.commit()
        return jsonify({"success": True, "mensaje": "Usuario registrado correctamente"})
    except mysql.connector.Error as err:
        return jsonify({"success": False, "mensaje": f"Error: {err}"}), 500
    finally:
        cursor.close()
        db.desconectar()

if __name__ == "__main__":
    app.run(debug=True)
