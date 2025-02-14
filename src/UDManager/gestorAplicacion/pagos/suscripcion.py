# src/UDManager/gestorAplicacion/pagos/suscripcion.py

from datetime import datetime, timedelta

class Suscripcion:
    def __init__(self, tipo="Ninguno", costo=0):
        self.nivel = tipo
        self.costo_anual = costo
        self.inicioSuscripcion = datetime.now()
        self.finSuscripcion = datetime.now() + timedelta(days=30)

    def verificacionVencimiento(self):
        return self.finSuscripcion >= datetime.now()

    def __str__(self):
        return f"Suscripción: {self.nivel} (Válida hasta: {self.finSuscripcion.strftime('%Y-%m-%d')})"
