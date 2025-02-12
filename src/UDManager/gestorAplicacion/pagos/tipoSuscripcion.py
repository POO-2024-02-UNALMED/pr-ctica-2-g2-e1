from enum import Enum

class TipoSuscripcion(Enum):
    NOTIENE = ("Sin suscripcion", 0, 0.0, False, False, 0, 0.0)
    ROOKIE = ("Rookie", 12000, 0.05, True, True, 0, 0.0)
    PROPLAYER = ("Pro Player", 20000, 0.08, True, True, 1, 0.1)
    MVP = ("MVP", 25000, 0.15, True, True, 4, 0.1)

    def __init__(self, nombre, precio, descuento, formativo, crearTorneo, reservasGratis, descBoletas):
        self.nombre = nombre
        self.precio = precio
        self.descuento = descuento
        self.formativo = formativo
        self.crearTorneo = crearTorneo
        self.reservasGratis = reservasGratis
        self.descBoletas = descBoletas