# src/UDManager/gestorAplicacion/inscripcion/joven.py

from src.UDManager.gestorAplicacion.entidades.persona import Persona

class Joven(Persona):
    listaJovenes = []

    def __init__(self, nombre="", apellido="", id=0, edad=0, experienciaJoven=0, eps="", nombreAcudiente="", telefonoAcudiente="", cedulaAcudiente=""):
        super().__init__(nombre, apellido, edad, id)
        self.experienciaJoven = experienciaJoven
        self.eps = eps
        self.nombreAcudiente = nombreAcudiente
        self.telefonoAcudiente = telefonoAcudiente
        self.cedulaAcudiente = cedulaAcudiente
        self.registrosEntrenamiento = []
        self.inscripcionPagada = False
        self.totalArticulos = 0
        Joven.listaJovenes.append(self)

    def getRol(self):
        return "Joven"

    def registrarEntrenamiento(self, registro):
        self.registrosEntrenamiento.append(registro)

    def darCategoria(self, exp):
        if exp < 6:
            return 1
        elif exp < 12:
            return 2
        else:
            return 3

    def __str__(self):
        return f"Joven: {self.getNombreCompleto()} - Experiencia: {self.experienciaJoven} meses"
