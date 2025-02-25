# src/UDManager/gestorAplicacion/inscripcion/entrenador.py

from src.UDManager.gestorAplicacion.entidades.persona import Persona
from src.UDManager.gestorAplicacion.entidades.trabajador import Trabajador

class Entrenador(Persona, Trabajador):
    def __init__(self, nombre="", apellido="", edad=0, deporte="", id=0):
        super().__init__(nombre=nombre, apellido=apellido, edad=edad, id=id, rol="Entrenador")
        self.deporte = deporte

    def getRol(self):
        return "Entrenador"

    def getDeporte(self):
        return self.deporte
    def setDeporte(self, deporte):
        self.deporte = deporte

    @staticmethod
    def entrenar():
        return "El entrenador se encuentra entrenando al joven"

    def entrenamiento(self):
        return "Entrenamiento genérico: trote ligero, ejercicios de calentamiento y estiramiento."

    def __str__(self):
        return f"Entrenador: {self.getNombreCompleto()} - Deporte: {self.deporte}"