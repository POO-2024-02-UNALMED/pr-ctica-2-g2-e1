# src/UDManager/gestorAplicacion/entidades/persona.py

from multimethod import multimethod
from abc import ABC, abstractmethod

class Persona(ABC):
    @multimethod
    def __init__(self, nombre: str = "", apellido: str = "", edad: int = 0, id: int = 0, **kwargs) -> None:
        super().__init__(**kwargs)
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.id = id

    # Sobrecarga 1: Recibe (id, nombre)
    @multimethod
    def __init__(self, id: int, nombre: str):
        # mandamos a la versión “default” usando argumentos con nombre
        self.__init__(nombre=nombre, id=id)

    # Sobrecarga 2: Recibe (apellido, id)
    @multimethod
    def __init__(self, apellido: str, id: int):
        # Llamada a la sobrecarga anterior (que recibe id y nombre), dejando nombre vacío
        self.__init__(id, "")
        # Asignamos el apellido recibido
        self.apellido = apellido



    def nombre(self, valor):
        self.nombre = valor

    def apellido(self):
        return self.apellido

    def apellido(self, valor):
        self.apellido = valor

    def edad(self):
        return self.edad

    def edad(self, valor):
        self.edad = valor

    def id(self):
        return self.id

    def id(self, valor):
        self.id = valor

    def getNombreCompleto(self):
        return f"{self.nombre} {self.apellido}"

    @abstractmethod
    def getRol(self):
        raise NotImplementedError("Debe implementar getRol() en la subclase.")

    def __str__(self):
        return self.getNombreCompleto()
