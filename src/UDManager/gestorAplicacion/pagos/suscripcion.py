from datetime import date, timedelta
from src.UDManager.gestorAplicacion.pagos.tipoSuscripcion import TipoSuscripcion

class Suscripcion:
    def __init__(self, tipoSuscripcion=TipoSuscripcion.NOTIENE):
        self.tipoSuscripcion = tipoSuscripcion
        self.inicioSuscripcion = date.today()
        self.finSuscripcion = date.today() + timedelta(days=30)

    def verificacionVencimiento(self):
        return self.finSuscripcion >= date.today()

    def __str__(self):
        return (f"Información de suscripción:\nTipo: {self.tipoSuscripcion.nombre}\n"
                f"Inicio: {self.inicioSuscripcion}\nFin: {self.finSuscripcion}")