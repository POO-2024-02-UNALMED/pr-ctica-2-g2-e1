from persona import Persona

class Trabajador(Persona):
    def __init__(self, nombre="", apellido="", rol="", edad=0):
        super().__init__(nombre, apellido, edad)
        self.rol = rol
        self.ocupado = False

    def getRol(self):
        return self.rol

    def __str__(self):
        return f"Trabajador: {self.getNombreCompleto()}, Rol: {self.rol}"
