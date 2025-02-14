# src/UDManager/gestorAplicacion/torneo/torneo.py

import random

class Torneo:
    torneos = []

    def __init__(self, deporte, equiposParticipantes, seguroMedico="", precioTotal=0):
        self.deporte = deporte
        self.equiposParticipantes = equiposParticipantes
        self.seguroMedico = seguroMedico
        self.precioTotal = precioTotal
        self.instalacion = None
        self.reglas = []
        self.arbitros = []
        self.reservas = []
        self.boletas = []
        self.idTorneo = len(Torneo.torneos) + 1
        Torneo.torneos.append(self)

    @staticmethod
    def setTorneos(lista):
        Torneo.torneos = lista

    @staticmethod
    def getTorneos():
        return Torneo.torneos

    def __str__(self):
        return f"Torneo {self.idTorneo}: {self.deporte} - Total: {self.precioTotal}"
