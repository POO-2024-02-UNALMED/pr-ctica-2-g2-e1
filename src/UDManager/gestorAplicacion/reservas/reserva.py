import random
from datetime import datetime

class Reserva:
    listaReservas = []

    def __init__(self, cliente, instalacion, fechaReserva, aPagar):
        # Generación del ID de la reserva
        self.ID = len(Reserva.listaReservas) + 1
        self.ID_pago = f"RES-{random.randint(100000, 999999)}"  # ID de pago en el formato RES-XXXXXX
        self.cliente = cliente
        self.instalacion = instalacion
        self.fechaReserva = fechaReserva  # Esto ahora será un objeto FechaReserva
        self.aPagar = aPagar
        self.pagada = False
        Reserva.listaReservas.append(self)
        instalacion.agregar_reserva(self)

    def __str__(self):
        return (f"Reserva {self.ID} (Pago: {self.ID_pago}) para {self.cliente} "
                f"en {self.instalacion.nombre}. De {self.fechaReserva.getInicioReserva()} "
                f"a {self.fechaReserva.getFinReserva()}. Total a pagar: {self.aPagar} - Pagada: {self.pagada}")

    # Métodos estáticos para manejar reservas
    @staticmethod
    def buscarReserva(ID):
        for r in Reserva.listaReservas:
            if r.ID == ID:
                return r
        return None

    @staticmethod
    def getListaReservas():
        return Reserva.listaReservas

    @staticmethod
    def setListaReservas(lista):
        Reserva.listaReservas = lista
