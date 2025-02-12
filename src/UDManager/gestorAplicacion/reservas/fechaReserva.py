from datetime import datetime

class FechaReserva:
    def __init__(self, inicioReserva, finReserva):
        self.inicioReserva = inicioReserva  # Objeto datetime
        self.finReserva = finReserva        # Objeto datetime

    def getInicioReserva(self):
        return self.inicioReserva

    def getFinReserva(self):
        return self.finReserva

    def __str__(self):
        return f"Fecha Reserva: Inicio: {self.inicioReserva}, Fin: {self.finReserva}"