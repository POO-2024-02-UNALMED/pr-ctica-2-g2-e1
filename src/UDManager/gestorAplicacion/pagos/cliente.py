# src/UDManager/gestorAplicacion/pagos/cliente.py

from src.UDManager.gestorAplicacion.entidades.persona import Persona
from src.UDManager.gestorAplicacion.pagos.suscripcion import Suscripcion
from multimethod import multimethod

class Cliente(Persona):
    listaClientes = []

    def __init__(self, nombre="", apellido="",edad=0, id=0,):
        super().__init__(nombre, apellido, edad, id)
        self.suscripcion = Suscripcion("Ninguno", 0)
        self.ID = id if id != 0 else len(Cliente.listaClientes) + 1
        Cliente.listaClientes.append(self)

    @multimethod
    @staticmethod
    def obtenerCliente():#Lista completa de clientes sin parametros

        return Cliente.listaClientes

    @multimethod
    @staticmethod
    def obtenerCliente(ID):#clientes por ID
        for cliente in Cliente.listaClientes:
            if cliente.ID == ID:
                return cliente
        return None

    @multimethod
    @staticmethod
    def obtenerCliente(nombre: str):#Clientes por nombre
        nombreBusqueda = nombre.lower()
        resultados = []
        for c in Cliente.listaClientes:
            if nombreBusqueda in c.nombre.lower():
                resultados.append(c)
        return resultados

    @staticmethod
    def getListaClientes():
        return Cliente.listaClientes

    @staticmethod
    def setListaClientes(lista):
        Cliente.listaClientes = lista

    def getRol(self):
        return "Cliente"

    def __str__(self):
        return (f"Cliente: {self.getNombreCompleto()} ID: {self.ID}\n  "
                f"Suscripción: {self.suscripcion.nivel}")
