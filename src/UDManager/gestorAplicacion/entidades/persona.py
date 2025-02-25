# src/UDManager/gestorAplicacion/entidades/persona.py
from abc import ABC, abstractmethod
import pickle

class Persona(ABC):
    def __init__(self, nombre="", apellido="", edad=0, id=0, **kwargs):
        super().__init__(**kwargs)  
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.id = id

    def getNombreCompleto(self):
        return f"{self.nombre} {self.apellido}"

    @abstractmethod
    def getRol(self):
        raise NotImplementedError("Debe implementar getRol() en la subclase.")

    def __str__(self):
        return self.getNombreCompleto()

