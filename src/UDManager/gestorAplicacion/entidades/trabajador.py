# src/UDManager/gestorAplicacion/entidades/trabajador.py


class Trabajador:
    def __init__(self, rol="", *args, **kwargs):
        self.rol = rol
        self.ocupado = False

    def getRol(self):
        return self.rol

    def isOcupado(self):
        return self.ocupado

    def setOcupado(self, ocupado):
        self.ocupado = ocupado
