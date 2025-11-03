from data_base.DAOusers import DAOusers
from data_base.connection import Connection
from routes.usuarios import Usuarios
from routes.lista_anime import ListaAnime
from routes.recomendaciones import Recomendaciones
from flask import Flask


def create_connection_with_prompts():
    host = input("Introduzca el host de la base de datos (localhost por defecto): ")
    user = input("Introduzca el usuario de la base de datos (root por defecto): ")
    password = input("Introduzca la contraseña de la base de datos (123456 por defecto): ")
    database = input("Introduzca el nombre de la base de datos (usuarios_anime por defecto): ")

    if host == "" and user == "" and password == "" and database == "":
        conexion = Connection().conectar()
    else:
        conexion = Connection(host, user, password, database).conectar()
    return conexion


class Api:
    def __init__(self, conexion):
        self.app = Flask(__name__)
        self.dao = DAOusers(conexion)
        self.rutas = Usuarios(self.app, self.dao)
        self.lista_anime = ListaAnime(self.app)
        self.recomendaciones = Recomendaciones(self.app)

    def encendido(self):
        self.app.run()


if __name__ == "__main__":
    conexion = create_connection_with_prompts()
    api = Api(conexion)
    api.encendido()