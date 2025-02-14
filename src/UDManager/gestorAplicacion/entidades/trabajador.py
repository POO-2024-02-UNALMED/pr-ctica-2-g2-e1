# src/UDManager/gestorAplicacion/entidades/trabajador.py

from src.UDManager.gestorAplicacion.entidades.persona import Persona

class Trabajador(Persona):
    def __init__(self, nombre="", apellido="", rol="", edad=0):
        super().__init__(nombre, apellido, edad)
        self.rol = rol
        self.ocupado = False

    def getRol(self):
        return self.rol

    def isOcupado(self):
        return self.ocupado

    def setOcupado(self, ocupado):
        self.ocupado = ocupado
