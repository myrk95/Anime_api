from DAOusers import DAOusers
from connection import Connection
from flask import Flask,jsonify, request as req

host = input("Introduzca el host de la base de datos (localhost por defecto):")
user = input("Introduzca el usuario de la base de datos (root por defecto):")
password = input("Introduzca la contraseña de la base de datos (123456 por defecto):")
database = input("Introduzca el nombre de la base de datos (carreras por defecto):")

if host == "" and user == "" and password == "" and database == "":
     conexion = Connection().conectar()

else:
     conexion = Connection(host,user,password,database).conectar()


class Api:

    def __init__(self, conexion):
        self.app = Flask(__name__)
        self.dao = DAOusers(conexion)
        self.rutas()
    
    def rutas(self):
            @self.app.route("/mostrar", methods=['GET'])
            def mostrar():
                datos = self.dao.mostrar_usuario()
                return jsonify([{"id": id, "nombre": nombre} for id, nombre in datos])
            
            @self.app.route("/crear_usuario", methods=['POST'])
            def crear_usuario():
                nombre = req.form["nombre"]
                nombre = self.dao.crear_carrera(nombre)
                return jsonify({"Nombre": nombre })

            @self.app.route("/modificar_carrera/<int:idcarreras>", methods=['PUT'])
            def actualizar(idcarreras):
                nuevo_nombre = req.form["nuevo_nombre"]
                nombre = self.dao.actualizar_carrera(nuevo_nombre,idcarreras)
                return jsonify ({"Nombre": nombre })

            @self.app.route("/eliminar/<int:idcarreras>", methods=['DELETE'])
            def eliminar(idcarreras):
                eliminar = self.dao.eliminar_carrera(idcarreras)
                if eliminar:
                     return jsonify({"Eliminado": eliminar})
                else:
                    return jsonify({"Error": "No se ha podido eliminar la carrera"})

                
    
    def encendido(self):
        self.app.run()
    
api = Api(conexion)
api.encendido()