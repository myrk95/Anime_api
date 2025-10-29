class Users:
    def __init__(self,nombre, apellidos, mail, password):
        self.setNombre(nombre)
        self.setApellidos(apellidos)
        self.setMail(mail)
        self.setPassword(password)

    def setNombre(self,nombre):
        self.__nombre = nombre

    def setApellidos(self,apellidos):
        self.__apellidos = apellidos
    
    def setMail(self,mail):
        self.__mail = mail
    
    def setPassword(self,password):
        self.__password = password

    def getNombre(self):
        return self.__nombre
    
    def getApellidos(self):
        return self.__apellidos
    
    def getMail(self):
        return self.__mail
    
    def getPassword(self):
        return self.__password
    
    
