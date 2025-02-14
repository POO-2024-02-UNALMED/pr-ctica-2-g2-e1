# src/UDManager/gestorAplicacion/reservas/fechaReserva.py

from datetime import datetime

class FechaReserva:
    def __init__(self, inicioReserva, finReserva):
        self.inicioReserva = inicioReserva
        self.finReserva = finReserva

    def getInicioReserva(self):
        return self.inicioReserva

    def getFinReserva(self):
        return self.finReserva
