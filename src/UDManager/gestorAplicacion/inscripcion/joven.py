from gestorAplicacion.entidades.persona import Persona

class Joven(Persona):
    listaJovenes = []  # Lista estática de jóvenes

    def __init__(self, nombre="", apellido="", id=None, edad=0, experienciaJoven=0, eps="",
                 nombreAcudiente="", telefonoAcudiente="", cedulaAcudiente=""):
        super().__init__(nombre, apellido, edad, id)
        self.experienciaJoven = experienciaJoven
        self.eps = eps
        self.nombreAcudiente = nombreAcudiente
        self.telefonoAcudiente = telefonoAcudiente
        self.cedulaAcudiente = cedulaAcudiente
        self.registrosEntrenamiento = []  # Lista de enteros
        self.inscripcionPagada = False
        self.totalArticulos = 0.0
        Joven.listaJovenes.append(self)

    def getRol(self):
        return "Joven"

    def agregarRegistroEntrenamiento(self, registro):
        self.registrosEntrenamiento.append(registro)

    def darCategoria(self, exp):
        if exp < 6:
            return 1
        elif exp < 12:
            return 2
        else:
            return 3

    def __str__(self):
        return f"Joven: {self.getNombreCompleto()}, Edad: {self.edad}, Experiencia: {self.experienciaJoven}"
