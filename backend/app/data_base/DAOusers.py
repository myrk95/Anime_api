# database/dao_usuarios_anime.py
from models.users import Users

class DAOusers:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def crear_usuario(self, nombre, apellidos, mail, password):
        self.cursor.execute(
            'INSERT INTO usuarios (nombre, apellidos, mail, password) VALUES (%s, %s, %s, %s)',
            (nombre, apellidos, mail, password)
        )
        self.connection.commit()
        return Users(nombre, apellidos, mail, password)

    def actualizar_usuario(self, idusuario, nuevo_nombre, nuevo_apellidos, nuevo_mail, nuevo_password):
        self.cursor.execute(
            'UPDATE usuarios SET nombre=%s, apellidos=%s, mail=%s, password=%s WHERE id_usuario=%s',
            (nuevo_nombre, nuevo_apellidos, nuevo_mail, nuevo_password, idusuario)
        )
        self.connection.commit()
        return self.cursor.rowcount > 0

    def eliminar_usuario(self, idusuario):
        self.cursor.execute('DELETE FROM usuarios WHERE id_usuario=%s', (idusuario,))
        self.connection.commit()
        if self.cursor.rowcount > 0:
            return True
        else:
            return False
    
    def autenticar_usuario(self, mail, password):
        self.cursor.execute('SELECT * FROM usuarios WHERE mail=%s AND password=%s', (mail, password))
        user = self.cursor.fetchone()
        if user:
            return user
        else:
            return None

    def mostrar_usuario_act(self, mail_actual):
        self.cursor.execute(
            'SELECT id_usuario, nombre, apellidos, mail, rol FROM usuarios WHERE mail=%s', (mail_actual,))
        return self.cursor.fetchone()
    
    def mostrar_usuarios(self, mail_actual):
        self.cursor.execute('SELECT rol FROM usuarios WHERE mail=%s', (mail_actual,))
        result = self.cursor.fetchone()
        if result and result[0] == 'admin':
            self.cursor.execute('SELECT id_usuario, nombre, apellidos, mail, rol FROM usuarios')
            return self.cursor.fetchall()
        else:
            return None  
    