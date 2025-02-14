# src/UDManager/gestorAplicacion/eventos/evento.py

from src.UDManager.gestorAplicacion.eventos.localidad import Localidad

class Evento:
    eventos = []

    def __init__(self):
        self.nombreEvento = ""
        self.tipoEvento = ""
        self.personajePrincipal = ""
        self.generoMusical = ""
        self.artistasInvitados = []
        self.lugarPrincipal = None
        self.localidades = []
        self.toldosPatrocinados = []
        self.foodTrucks = []
        self.personalSeguridad = []
        self.personalMedico = []
        self.reservas = []
        self.boletas = []

    @staticmethod
    def getEventos():
        return Evento.eventos

    @staticmethod
    def setEventos(lista):
        Evento.eventos = lista

    def __str__(self):
        return f"Evento: {self.nombreEvento} - Tipo: {self.tipoEvento}"
