# src/UDManager/gestorAplicacion/inscripcion/deporteFormativo.py

class DeporteFormativo:
    def __init__(self):
        self.nombre = ""
        self.edad = 0
        self.eps = ""
        self.acudiente = ""
        self.deporteDeseado = ""
        self.experienciaMeses = 0
        self.categoriaEquipo = ""
        self.categoriaEntrenador = ""
        self.horario = ""

    def clasificarYAsignar(self):
        if self.experienciaMeses < 6:
            self.categoriaEquipo = "Categoría 1"
            self.categoriaEntrenador = "Entrenador Categoría 1"
        elif self.experienciaMeses <= 12:
            self.categoriaEquipo = "Categoría 2"
            self.categoriaEntrenador = "Entrenador Categoría 2"
        else:
            self.categoriaEquipo = "Categoría 3"
            self.categoriaEntrenador = "Entrenador Categoría 3"

        if self.edad <= 12:
            self.horario = "Mañana: 6 AM - 12 M"
        else:
            self.horario = "Tarde: 1 PM - 8 PM"

    def __str__(self):
        return f"DeporteFormativo: {self.nombre} - {self.deporteDeseado}"
