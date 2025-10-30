# database/dao_usuarios_anime.py
from users import Users

class DAOusers:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def crear_usuario(self, nombre, apellidos, mail, password):
        self.cursor.execute(
            'INSERT INTO users (nombre, apellidos, mail, password) VALUES (%s, %s, %s, %s)',
            (nombre, apellidos, mail, password)
        )
        self.connection.commit()
        return Users(nombre, apellidos, mail, password)

    def actualizar_usuario(self, idusuario, nuevo_nombre, nuevo_apellidos, nuevo_mail, nuevo_password):
        self.cursor.execute(
            'UPDATE users SET nombre=%s, apellidos=%s, mail=%s, password=%s WHERE idusers=%s',
            (nuevo_nombre, nuevo_apellidos, nuevo_mail, nuevo_password, idusuario)
        )
        self.connection.commit()
        return self.cursor.rowcount > 0

    def eliminar_usuario(self, idusuario):
        self.cursor.execute('DELETE FROM users WHERE idusers=%s', (idusuario,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def mostrar_usuarios(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()
