# src/UDManager/gestorAplicacion/reservas/reserva.py

import random
from datetime import datetime

class Reserva:
    listaReservas = []

    def __init__(self, cliente, instalacion, fechaReserva, aPagar):
        self.ID = len(Reserva.listaReservas) + 1
        self.cliente = cliente
        self.instalacion = instalacion
        self.fechaReserva = fechaReserva
        self.aPagar = aPagar
        self.pagada = False
        self.equipo1 = None
        self.equipo2 = None
        self.grupoFormativo = None
        self.arbitro = None
        Reserva.listaReservas.append(self)
        instalacion.agregar_reserva(self)

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

    def __str__(self):
        return (f"Reserva {self.ID} para {self.cliente.getNombreCompleto()} en {self.instalacion.nombre}. "
                f"Total a pagar: {self.aPagar} - Pagada: {self.pagada}")
