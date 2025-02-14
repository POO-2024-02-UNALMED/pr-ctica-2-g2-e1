# src/UDManager/gestorAplicacion/torneo/equipo.py

class Equipo:
    def __init__(self, nombreEquipo):
        self.idEquipo = 0
        self.nombreEquipo = nombreEquipo
        self.jugadores = []

    def setJugador(self, nombreJugador):
        self.jugadores.append(nombreJugador)

    def __str__(self):
        return f"Equipo: {self.nombreEquipo} - Jugadores: {', '.join(self.jugadores)}"
