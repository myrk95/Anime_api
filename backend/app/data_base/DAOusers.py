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
        return self.cursor.rowcount > 0
    
    def autenticar_usuario(self, mail, password):
        # Select explicit columns so we don't rely on DB column ordering
        self.cursor.execute(
            'SELECT id_usuario, nombre, apellidos, mail, rol FROM usuarios WHERE mail=%s AND password=%s',
            (mail, password)
        )
        user = self.cursor.fetchone()
        if user:
            return user
        else:
            return None

    def mostrar_usuario(self, mail):
        """Get a single user's information"""
        self.cursor.execute(
            'SELECT id_usuario, nombre, apellidos, mail, rol FROM usuarios WHERE mail=%s', 
            (mail,)
        )
        user = self.cursor.fetchone()
        if user:
            return {
                'id': user[0],
                'nombre': user[1],
                'apellidos': user[2],
                'mail': user[3],
                'rol': user[4]
            }
        return None
    
    def mostrar_usuarios(self):
        """Get all users without role check"""
        self.cursor.execute('SELECT id_usuario, nombre, apellidos, mail, rol FROM usuarios')
        users = self.cursor.fetchall()
        return [{
            'id': user[0],
            'nombre': user[1],
            'apellidos': user[2],
            'mail': user[3],
            'rol': user[4]
        } for user in users]
    
    def get_user_role(self, mail):
        """Get user's role"""
        self.cursor.execute('SELECT rol FROM usuarios WHERE mail=%s', (mail,))
        result = self.cursor.fetchone()
        return result[0] if result else None