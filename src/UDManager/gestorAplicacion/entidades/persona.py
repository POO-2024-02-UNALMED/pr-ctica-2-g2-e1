# src/UDManager/gestorAplicacion/entidades/persona.py
import pickle
from abc import ABC, abstractmethod

class Persona(ABC):
    def __init__(self, nombre="", apellido="", edad=0, id=0, **kwargs):
        super().__init__(**kwargs)
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.id = id

    def nombre(self):
        return self.nombre

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
