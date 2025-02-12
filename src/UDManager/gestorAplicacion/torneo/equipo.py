class Equipo:
    counter = 0

    def __init__(self, nombreEquipo=""):
        Equipo.counter += 1
        self.idEquipo = Equipo.counter
        self.nombreEquipo = nombreEquipo
        self.jugadores = []

    def agregarJugador(self, nombreJugador):
        self.jugadores.append(nombreJugador)

    def __str__(self):
        return f"Equipo: {self.nombreEquipo} (ID: {self.idEquipo})"