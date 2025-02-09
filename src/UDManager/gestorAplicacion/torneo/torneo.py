class Torneo:
    torneos = []  # Lista estática de torneos

    def __init__(self, deporte="", equiposParticipantes=None, seguroMedico="", precioTotal=0.0):
        self.deporte = deporte
        self.equiposParticipantes = equiposParticipantes if equiposParticipantes is not None else []
        self.seguroMedico = seguroMedico
        self.costoSeguroMedico = 0.0
        self.precioTotal = precioTotal
        self.instalacion = None
        self.reglas = []
        self.arbitros = []
        self.reservas = []
        self.boletas = []
        self.idTorneo = 0
        Torneo.torneos.append(self)

    def agregarSeguro(self, seguro, costo):
        self.seguroMedico = seguro
        self.precioTotal += costo

    def setDeporte(self, num):
        if num == 1:
            self.deporte = "Futbol"
        elif num == 2:
            self.deporte = "Baloncesto"
        elif num == 3:
            self.deporte = "Natacion"
        elif num == 4:
            self.deporte = "Voleibol"
        else:
            self.deporte = "Indefinido"

    def getDeporte(self):
        return self.deporte

    def getInstalaciones(self, num, inst):
        instalaciones = []
        if num == 1:
            instalaciones.extend(inst[0:4])
        elif num == 2:
            instalaciones.extend(inst[4:7])
        elif num == 3:
            instalaciones.extend(inst[7:10])
        elif num == 4:
            instalaciones.extend(inst[10:12])
        return instalaciones

    def setInstalacion(self, instalacionIndex, inst):
        if self.deporte == "Futbol":
            self.instalacion = inst[instalacionIndex-1]
        elif self.deporte == "Baloncesto":
            self.instalacion = inst[instalacionIndex-1+4]
        elif self.deporte == "Natacion":
            self.instalacion = inst[instalacionIndex-1+7]
        elif self.deporte == "Voleibol":
            self.instalacion = inst[instalacionIndex-1+10]

    def setReglas(self, reglas):
        self.reglas = reglas

    def setEquiposParticipantes(self, equipos):
        self.equiposParticipantes = equipos

    @classmethod
    def setTorneos(cls, listaTorneos):
        cls.torneos = listaTorneos

    @classmethod
    def getTorneos(cls):
        return cls.torneos

    def getArbitros(self):
        return self.arbitros

    def setArbitros(self, arbitros):
        self.arbitros = list(arbitros)

    def agregarArbitro(self, arbitro):
        self.arbitros.append(arbitro)

    def setIdTorneo(self, idTorneo):
        self.idTorneo = idTorneo

    def calcularPrecio(self):
        if self.equiposParticipantes:
            self.precioTotal = len(self.equiposParticipantes) * 100
        if self.seguroMedico:
            self.precioTotal += self.costoSeguroMedico

    def __str__(self):
        return f"Torneo: {self.deporte}, Precio Total: {self.precioTotal}"
