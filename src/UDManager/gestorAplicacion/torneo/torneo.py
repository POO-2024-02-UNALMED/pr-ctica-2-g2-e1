# src/UDManager/gestorAplicacion/torneo/torneo.py

import random
import time

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
        self.pagado = False
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.ticket_id = 0
        self.pago_id = 0
        Torneo.torneos.append(self)

    def generar_ticket_id(self):
        # Usamos el tiempo actual (timestamp) y un número aleatorio para asegurar la unicidad.
        if not self.ticket_id:  # Verificamos si ya tiene un ticket_id asignado
            timestamp = int(time.time() * 1000)  # Tiempo en milisegundos
            random_number = random.randint(1000, 9999)  # Un número aleatorio para mayor unicidad
            self.ticket_id = f"TICKET-{timestamp}-{random_number}"  # Genera un ticket ID único
        return self.ticket_id


    def generar_pago_id(self):
        self.pago_id = f"PAY-{random.randint(100000, 999999)}"

    @staticmethod
    def setTorneos(lista):
        Torneo.torneos = lista

    @staticmethod
    def getTorneos():
        return Torneo.torneos

    def __str__(self):
        return f"Nombre: {self.nombre} - Deporte: {self.deporte} - Pagado: {'Si' if self.pagado else 'No'} - ID: {self.ticket_id}"
