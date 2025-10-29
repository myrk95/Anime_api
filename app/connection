import mysql.connector

class Connection:
    def __init__(self, host="localhost", user="root", password="123456", database="usuarios_anime"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def conectar(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        return self.connection
    
    def desconectar(self):
        if self.connection:
            self.connection.close()
            self.connection = None