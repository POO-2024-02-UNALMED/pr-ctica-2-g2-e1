# src/UDManager/gestorAplicacion/inscripcion/grupoFormativo.py

from src.UDManager.gestorAplicacion.inscripcion.joven import Joven

class GrupoFormativo:
    grupoFormativos = []

    def __init__(self, deporte="", instalacion=None, entrenador=None):
        self.deporte = deporte
        self.instalacion = instalacion
        self.entrenador = entrenador
        self.jovenes = []
        self.reserva = None

    def addJoven(self, joven):
        self.jovenes.append(joven)

    @staticmethod
    def getGrupoFormativos():
        return GrupoFormativo.grupoFormativos

    @staticmethod
    def setGrupoFormativos(lista):
        GrupoFormativo.grupoFormativos = lista

    def deleteJoven(self, joven):
        if joven in self.jovenes:
            self.jovenes.remove(joven)

    def resetJovenes(self):
        self.jovenes = []

    def __str__(self):
        return f"GrupoFormativo de {self.deporte} - Entrenador: {self.entrenador}"
