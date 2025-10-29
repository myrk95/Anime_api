class Users:
    def __init__(self,nombre):
        self.setNombre(nombre)

    def setNombre(self,nombre):
        self.__nombre = nombre

    def getNombre(self):
        return self.__nombre
