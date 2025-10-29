from users import Users

class DAOusers:
    def __init__(self,connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.user = Users(None, None, None, None)

    def crear_usuario(self, nombre, apellidos, mail, password):
        self.user.setNombre(nombre)
        self.user.setApellidos(apellidos)
        self.user.setMail(mail)
        self.user.setPassword(password)
        self.connection.commit()
        self.cursor.execute('INSERT INTO users(nombre, apellidos, mail, password) VALUES (%s, %s, %s, %s)',(self.user.getNombre(), self.user.getApellidos(), self.user.getMail(), self.user.getPassword()))
        return self.user.getNombre(), self.user.getApellidos(), self.user.getMail()
    
    def actualizar_usuario(self,nuevo_nombre, nuevo_apellidos, nuevo_mail, nuevo_password):
        self.cursor.execute('UPDATE users SET nombre=%s, apellidos=%s, mail=%s, password=%s WHERE idusers=%s',(nuevo_nombre, nuevo_apellidos, nuevo_mail, nuevo_password))
        self.connection.commit()
        self.user.setNombre(nuevo_nombre)
        self.user.setApellidos(nuevo_apellidos)
        self.user.setMail(nuevo_mail)
        self.user.setPassword(nuevo_password)
        return self.user.getNombre(), self.user.getApellidos(), self.user.getMail()

    def eliminar_usuario(self, idusuario):
        self.cursor.execute('DELETE FROM users WHERE idusers= %s', (idusuario,))
        self.connection.commit()
        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    def mostrar_usuario(self):
        self.cursor.execute('SELECT * FROM users')
        resultado = self.cursor.fetchall()
        return resultado

