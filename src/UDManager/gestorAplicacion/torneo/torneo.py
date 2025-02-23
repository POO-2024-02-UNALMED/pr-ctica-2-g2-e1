# src/UDManager/gestorAplicacion/torneo/torneo.py

import random

class Torneo:
    torneos = []

    def __init__(self, deporte, equiposParticipantes,fechaInicio, fechaFin, seguroMedico="", precioTotal=30000):
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
        self.nombre = "Torneo"
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.ticket_id = 0  # We will generate this later
        self.pago_id = 0 # We will generate this ID as well
        Torneo.torneos.append(self)

    def generar_ticket_id(self):
        # Only generate ticket ID if it hasn't been generated already
        if not self.ticket_id:
            self.ticket_id = f"TICKET-{random.randint(100000, 999999)}"
        else:
            print("ID de boletas ya generado.")

    def generar_pago_id(self):
        # Generate a unique payment ID using a random integer
        self.pago_id = f"PAY-{random.randint(100000, 999999)}"

    @staticmethod
    def setTorneos(lista):
        Torneo.torneos = lista

    @staticmethod
    def getTorneos():
        return Torneo.torneos

    def __str__(self):
        return "Hola"
