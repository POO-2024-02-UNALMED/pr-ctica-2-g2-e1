from gestorAplicacion.entidades.persona import Persona
from gestorAplicacion.pagos.suscripcion import Suscripcion
from gestorAplicacion.pagos.tipoSuscripcion import TipoSuscripcion

class Cliente(Persona):
    listaClientes = []  # Lista estática de clientes

    def __init__(self, nombre, apellido, edad, id=None):
        super().__init__(nombre, apellido, edad, id)
        if id is None:
            self.suscripcion = Suscripcion(TipoSuscripcion.NOTIENE)
            self.id = len(Cliente.listaClientes) + 1
            Cliente.listaClientes.append(self)
        else:
            self.suscripcion = None
            self.id = id

    @classmethod
    def obtenerCliente(cls, id):
        for cliente in cls.listaClientes:
            if cliente.id == id:
                return cliente
        return None

    def getRol(self):
        return "Cliente"

    def __str__(self):
        susc = self.suscripcion.tipoSuscripcion.nombre if self.suscripcion else "None"
        return (f"Cliente:\nID: {self.id}\nNombre: {self.nombre}\nApellido: {self.apellido}\n"
                f"Edad: {self.edad}\nSuscripción: {susc}")