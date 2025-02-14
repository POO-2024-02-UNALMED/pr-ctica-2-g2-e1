# src/UDManager/gestorAplicacion/inscripcion/entrenador.py

from src.UDManager.gestorAplicacion.entidades.persona import Persona

class Entrenador(Persona):
    def __init__(self, nombre="", apellido="", edad=0, deporte=""):
        super().__init__(nombre, apellido, edad)
        self.deporte = deporte

    def getRol(self):
        return "Entrenador"

    def __str__(self):
        return f"Entrenador: {self.getNombreCompleto()} - Deporte: {self.deporte}"
