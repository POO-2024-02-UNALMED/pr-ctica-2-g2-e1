# src/UDManager/gestorAplicacion/pagos/cliente.py

from src.UDManager.gestorAplicacion.entidades.persona import Persona
from src.UDManager.gestorAplicacion.pagos.suscripcion import Suscripcion

class Cliente(Persona):
    listaClientes = []

    def __init__(self, nombre="", apellido="",edad=0, id=0,):
        super().__init__(nombre, apellido, edad, id)
        self.suscripcion = Suscripcion("Ninguno", 0)
        self.ID = id if id != 0 else len(Cliente.listaClientes) + 1
        Cliente.listaClientes.append(self)

    @staticmethod
    def obtenerCliente(ID):
        for cliente in Cliente.listaClientes:
            if cliente.ID == ID:
                return cliente
        return None

    @staticmethod
    def getListaClientes():
        return Cliente.listaClientes

    @staticmethod
    def setListaClientes(lista):
        Cliente.listaClientes = lista

    def getRol(self):
        return "Cliente"

    def __str__(self):
        return (f"Cliente: {self.getNombreCompleto()} (ID: {self.ID})\n"
                f"Suscripción: {self.suscripcion.nivel}")
