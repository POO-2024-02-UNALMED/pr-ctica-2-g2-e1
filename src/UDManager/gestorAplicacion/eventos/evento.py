# src/UDManager/gestorAplicacion/eventos/evento.py

#from src.UDManager.gestorAplicacion.eventos.localidad import Localidad

class Evento:
    eventos = []

    def __init__(self,nombre,tipoEvento,personajePrincipal,reserva):
        self.nombre = nombre
        self.ID = len(Evento.eventos) + 1
        self.tipoEvento = tipoEvento
        self.personajePrincipal = personajePrincipal
        self.reserva = reserva
        self.boletas = []

        Evento.eventos.append(self)

    @staticmethod
    def getEventos():
        return Evento.eventos

    @staticmethod
    def setEventos(lista):
        Evento.eventos = lista

    def __str__(self):
        ultimo = "Cantante: " + self.personajePrincipal if self.tipoEvento == "Concierto" else ""
        return f"Evento: {self.nombre} \n Tipo: {self.tipoEvento} \n ID: {self.ID}  " + ultimo

