from flask import Flask, jsonify, request as req
from data_base.DAOusers import DAOusers

class Usuarios:
    def __init__(self, app: Flask, dao: DAOusers):
        self.app = app
        self.dao = dao
        self.rutas()

    def rutas(self):
        @self.app.route("/autenticar_usuario", methods=["POST"])
        def autenticar_usuario():
            data = req.get_json()
            mail = data.get("mail")
            password = data.get("password")
            user = self.dao.autenticar_usuario(mail, password)
            if user:
                return jsonify({
                    "mensaje": "Login correcto",
                    "id": user[0],
                    "nombre": user[1],
                    "apellidos": user[2],
                    "mail": user[3],
                    "rol": user[4]
                })
            else:
                return jsonify({"error": "Correo o contraseña incorrectos"}), 401

        @self.app.route("/mostrar_usuario", methods=["GET"])
        def mostrar_usuario():
            mail = req.args.get("mail")  
            if not mail:
                return jsonify({"error": "Debes indicar el mail"}), 400

            user = self.dao.mostrar_usuario(mail)
            if user:
                return jsonify({
                    "id": user[0],
                    "nombre": user[1],
                    "apellidos": user[2],
                    "mail": user[3],
                    "rol": user[4]
                })
            else:
                return jsonify({"error": "Usuario no encontrado"}), 404

        @self.app.route("/mostrar_usuarios", methods=["GET"])
        def mostrar_usuarios():
            mail_actual = req.args.get("mail")  # el mail del que consulta
            if not mail_actual:
                return jsonify({"error": "Debes indicar el mail"}), 400

            datos = self.dao.mostrar_usuarios(mail_actual)
            if datos:
                return jsonify([
                    {
                        "id": idu,
                        "nombre": n,
                        "apellidos": a,
                        "mail": m,
                        "rol": r
                    }
                    for idu, n, a, m, r in datos
                ])
            else:
                return jsonify({"error": "No tienes permisos o no hay usuarios"}), 403
            
        @self.app.route("/registrar_usuario", methods=["POST"])
        def registrar_usuario():
            datos = req.get_json(force=True)
            nombre = datos.get("nombre")
            apellidos = datos.get("apellidos")
            mail = datos.get("mail")
            password = datos.get("password")

            if not all([nombre, apellidos, mail, password]):
                return jsonify({"error": "Faltan datos"}), 400

            user = self.dao.crear_usuario(nombre, apellidos, mail, password)
            return jsonify({
                "mensaje": "Usuario creado correctamente",
                "nombre": user.getNombre(),
                "apellidos": user.getApellidos(),
                "mail": user.getMail()
            })

        @self.app.route("/actualizar_usuario/<int:idusuario>", methods=["PUT"])
        def actualizar_usuario(idusuario):
            nuevo_nombre = req.form.get("nombre")
            nuevo_apellidos = req.form.get("apellidos")
            nuevo_mail = req.form.get("mail")
            nuevo_password = req.form.get("password")

            actualizado = self.dao.actualizar_usuario(
                idusuario, nuevo_nombre, nuevo_apellidos, nuevo_mail, nuevo_password
            )

            if actualizado:
                return jsonify({"mensaje": "Usuario actualizado correctamente"})
            else:
                return jsonify({"error": "No se pudo actualizar el usuario"}), 400

        @self.app.route("/eliminar_usuario/<int:idusuario>", methods=["DELETE"])
        def eliminar_usuario(idusuario):
            eliminado = self.dao.eliminar_usuario(idusuario)
            if eliminado:
                return jsonify({"mensaje": "Usuario eliminado correctamente"})
            else:
                return jsonify({"error": "No se pudo eliminar el usuario"}), 400
