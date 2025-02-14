# src/UDManager/gestorAplicacion/pagos/boleta.py

import random

class Boleta:
    listaBoletas = []

    def __init__(self, tipoEvento, precio, cliente):
        self.ID = random.randint(100000, 999999)
        self.tipoEvento = tipoEvento
        self.precio = precio
        self.cliente = cliente
        self.pagada = False
        Boleta.listaBoletas.append(self)

    @staticmethod
    def buscarBoleta(ID):
        for boleta in Boleta.listaBoletas:
            if boleta.ID == ID:
                return boleta
        return None

    def __str__(self):
        return (f"Boleta ID: {self.ID}\nCliente: {self.cliente.getNombreCompleto()}\n"
                f"Tipo de Evento: {self.tipoEvento}\nTotal: {self.precio}")
