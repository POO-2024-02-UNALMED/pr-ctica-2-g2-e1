class Instalacion:
    listaInstalaciones = []

    def __init__(self, nombre, deporte, precioHora, horarios=None, reservas=None):
        self.nombre = nombre
        self.deporte = deporte
        self.precioHora = precioHora
        self.id = len(Instalacion.listaInstalaciones) + 1
        self.horarios = horarios if horarios is not None else []
        self.reservas = reservas if reservas is not None else []
        self.localidades = []
        Instalacion.listaInstalaciones.append(self)

    @staticmethod
    def deporteViaNumero(opcion):
        if opcion == 1:
            return "Futbol"
        elif opcion == 2:
            return "Baloncesto"
        elif opcion == 3:
            return "Natacion"
        elif opcion == 4:
            return "Voleibol"
        else:
            return None

    @staticmethod
    def crearInstalaciones():
        Instalacion.listaInstalaciones.clear()
        Instalacion("Cancha F11 1", "Futbol", 3000)
        Instalacion("Cancha F11 2", "Futbol", 3000)
        Instalacion("Cancha F9", "Futbol", 2000)
        Instalacion("Cancha F7", "Futbol", 1000)
        Instalacion("Coliseo", "Baloncesto", 4000)
        Instalacion("Cancha techada 1", "Baloncesto", 1000)
        Instalacion("Cancha techada 2", "Baloncesto", 1000)
        Instalacion("Piscina olimpica", "Natacion", 6000)
        Instalacion("Piscina semiolimpica", "Natacion", 4000)
        Instalacion("Piscina infantil", "Natacion", 2000)
        Instalacion("Cancha de cemento", "Voleibol", 3000)
        Instalacion("Cancha de arena", "Voleibol", 2000)

    @staticmethod
    def obtenerInstalacion(id):
        for inst in Instalacion.listaInstalaciones:
            if inst.id == id:
                return inst
        return None

    def __str__(self):
        return (f"Instalacion:\nID: {self.id}\nNombre: {self.nombre}\nDeporte: {self.deporte}\n"
                f"Precio/hora: {self.precioHora}")
