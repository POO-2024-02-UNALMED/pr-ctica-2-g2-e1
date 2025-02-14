# src/UDManager/gestorAplicacion/pagos/tipoSuscripcion.py

from enum import Enum

class TipoSuscripcion(Enum):
    NOTIENE = ("Sin suscripción", 0, 0, False, False, 0, 0)
    ROOKIE = ("Rookie", 12000, 0.05, True, True, 0, 0)
    PROPLAYER = ("ProPlayer", 20000, 0.08, True, True, 1, 0.1)
    MVP = ("MVP", 25000, 0.15, True, True, 4, 0.1)

    def __init__(self, nombre, precio, descuento, formativo, crearTorneo, reservasGratis, descBoletas):
        self.nombre = nombre
        self.precio = precio
        self.descuento = descuento
        self.formativo = formativo
        self.crearTorneo = crearTorneo
        self.reservasGratis = reservasGratis
        self.descBoletas = descBoletas

    def getNombre(self):
        return self.nombre

    def getPrecio(self):
        return self.precio

    def getDescuento(self):
        return self.descuento

    def isFormativo(self):
        return self.formativo

    def isCrearTorneo(self):
        return self.crearTorneo

    def getReservasGratis(self):
        return self.reservasGratis

    def getDescBoletas(self):
        return self.descBoletas
