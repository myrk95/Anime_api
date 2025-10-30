from connection import Connection  # si la classe està en connection.py
import mysql.connector

# Crear la instància
db = Connection(host="localhost", user="root", password="123456", database="usuarios_anime")

# Conectar
conn = db.conectar()
cursor = conn.cursor()

# Exemple: obtenir tots els usuaris
cursor.execute("SELECT * FROM usuarios")
resultados = cursor.fetchall()

for usuario in resultados:
    print(usuario)

# Tancar connexió
cursor.close()
db.desconectar()
