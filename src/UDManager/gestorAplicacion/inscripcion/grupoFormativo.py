class GrupoFormativo:
    grupoFormativos = []  # Lista estática de grupos formativos

    def __init__(self, deporte="", instalacion=None, entrenador=None):
        self.deporte = deporte
        self.instalacion = instalacion  # Por ejemplo, un objeto Instalacion
        self.entrenador = entrenador    # Por ejemplo, un objeto Entrenador
        self.jovenes = []               # Lista de objetos Joven
        self.reserva = None           # Objeto Reserva (opcional)
        GrupoFormativo.grupoFormativos.append(self)

    def addJoven(self, joven):
        self.jovenes.append(joven)

    def deleteJoven(self, joven):
        if joven in self.jovenes:
            self.jovenes.remove(joven)

    def resetJovenes(self):
        self.jovenes = []

    def __str__(self):
        return f"Grupo Formativo de {self.deporte} con {len(self.jovenes)} jóvenes"
