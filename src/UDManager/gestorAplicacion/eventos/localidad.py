# src/UDManager/gestorAplicacion/eventos/localidad.py

class Localidad:
    def __init__(self, instalacion, ubicacion, capacidad, precioSugerido=None):
        self.instalacionLocalidad = instalacion
        self.ubicacion = ubicacion
        self.capacidad = capacidad
        if precioSugerido is None:
            ps = int(round(50000 + capacidad * 0.01))
            self.precioSugerido = ps
        else:
            self.precioSugerido = precioSugerido
        self.division = False
        self.menores = False
        self.vip = False

    def __str__(self):
        return f"Localidad: {self.ubicacion} - Capacidad: {self.capacidad} - Precio sugerido: {self.precioSugerido}"
