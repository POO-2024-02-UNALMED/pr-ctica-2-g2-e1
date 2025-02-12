from abc import ABC, abstractmethod

class Persona(ABC):
    def __init__(self, nombre="", apellido="", edad=0, id=None):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.id = id

    @abstractmethod
    def getRol(self):
        pass

    def getNombreCompleto(self):
        return f"{self.nombre} {self.apellido}"

    def __str__(self):
        return self.getNombreCompleto()
