class Localidad:
    def __init__(self, instalacion=None, ubicacion="", capacidad=0, precioSugerido=None):
        self.instalacionLocalidad = instalacion
        self.ubicacion = ubicacion
        self.capacidad = capacidad
        self.division = False
        self.menores = False
        self.vip = False
        if precioSugerido is None:
            self.precioSugerido = round(50000 + capacidad * 0.01)
        else:
            self.precioSugerido = precioSugerido

    def __str__(self):
        return f"Localidad: {self.ubicacion} (Capacidad: {self.capacidad})"
