class Evento:
    eventos = []  # Lista estática de eventos

    def __init__(self):
        self.nombreEvento = ""
        self.tipoEvento = ""
        self.personajePrincipal = ""
        self.generoMusical = ""
        self.artistasInvitados = []  # Lista de cadenas
        self.lugarPrincipal = None   # Por ejemplo, un objeto Instalacion
        self.localidades = []        # Lista de objetos Localidad
        self.toldosPatrocinados = []
        self.foodTrucks = []
        self.personalSeguridad = []  # Lista de Trabajador
        self.personalMedico = []     # Lista de Trabajador
        self.reservas = []           # Lista de Reserva
        self.boletas = []            # Lista de Boleta

    def __str__(self):
        return self.nombreEvento
