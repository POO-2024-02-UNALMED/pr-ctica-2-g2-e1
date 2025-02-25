# src/UDManager/gestorAplicacion/entidades/persona.py
import pickle
from abc import ABC, abstractmethod

class Persona(ABC):
    def __init__(self, nombre="", apellido="", edad=0, id=0, **kwargs):
        super().__init__(**kwargs)
        self._nombre = nombre
        self._apellido = apellido
        self._edad = edad
        self._id = id

    def nombre(self):
        return self._nombre

    def nombre(self, valor):
        self._nombre = valor

    def apellido(self):
        return self._apellido

    def apellido(self, valor):
        self._apellido = valor

    def edad(self):
        return self._edad

    def edad(self, valor):
        self._edad = valor

    def id(self):
        return self._id

    def id(self, valor):
        self._id = valor

    def getNombreCompleto(self):
        return f"{self._nombre} {self._apellido}"

    @abstractmethod
    def getRol(self):
        raise NotImplementedError("Debe implementar getRol() en la subclase.")

    def __str__(self):
        return self.getNombreCompleto()
