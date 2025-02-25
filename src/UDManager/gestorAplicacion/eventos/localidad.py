# src/UDManager/gestorAplicacion/eventos/localidad.py

class Localidad:
    def __init__(self, instalacion, ubicacion, capacidad, precioSugerido=None):
        self._instalacionLocalidad = instalacion
        self._ubicacion = ubicacion
        self._capacidad = capacidad
        if precioSugerido is None:
            ps = int(round(50000 + capacidad * 0.01))
            self._precioSugerido = ps
        else:
            self._precioSugerido = precioSugerido
        self._division = False
        self._menores = False
        self._vip = False

    def __str__(self):
        return f"Localidad: {self._ubicacion} - Capacidad: {self._capacidad} - Precio sugerido: {self._precioSugerido}"
