import pickle
import os
from tkinter import messagebox
from src.UDManager.baseDatos.serializador import Serializador
from src.UDManager.baseDatos.deserializador import Deserializador
from src.UDManager.gestorAplicacion.eventos.evento import Evento
from src.UDManager.gestorAplicacion.inscripcion.joven import Joven
from src.UDManager.gestorAplicacion.inscripcion.grupoFormativo import GrupoFormativo
from src.UDManager.gestorAplicacion.inscripcion.tiendaEscuela import TiendaEscuela
from src.UDManager.gestorAplicacion.pagos.cliente import Cliente
from src.UDManager.gestorAplicacion.pagos.boleta import Boleta
from src.UDManager.gestorAplicacion.reservas.reserva import Reserva
from src.UDManager.gestorAplicacion.reservas.instalacion import Instalacion
from src.UDManager.gestorAplicacion.torneo.torneo import Torneo

class Database:
    def __init__(self, eventos, jovenes, grupoFormativos, tienda, clientes, boletas, reservas, instalaciones, torneos):
        self.eventos = eventos
        self.jovenes = jovenes
        self.grupoFormativos = grupoFormativos
        self.tienda = tienda
        self.clientes = clientes
        self.boletas = boletas
        self.reservas = reservas
        self.instalaciones = instalaciones
        self.torneos = torneos

class DataManager:
    filePath = "database.pkl"

    @staticmethod
    def saveData():
        db = Database(
            Evento.eventos,
            Joven.listaJovenes,
            GrupoFormativo.grupoFormativos,
            tiendaEscuela,
            Cliente.listaClientes,
            Boleta.listaBoletas,
            Reserva.listaReservas,
            Instalacion.listaInstalaciones,
            Torneo.torneos
        )
        if Serializador.serializar(db, DataManager.filePath):
            messagebox.showinfo("Guardar", "Datos guardados correctamente.")
        else:
            messagebox.showerror("Error", "Error al guardar los datos.")

    @staticmethod
    def loadData():
        db = Deserializador.deserializar(DataManager.filePath)
        if db is not None:
            Evento.eventos = db.eventos
            Joven.listaJovenes = db.jovenes
            GrupoFormativo.grupoFormativos = db.grupoFormativos
            global tiendaEscuela
            tiendaEscuela = db.tienda if db.tienda is not None else TiendaEscuela()
            Cliente.listaClientes = db.clientes
            Boleta.listaBoletas = db.boletas
            Reserva.listaReservas = db.reservas
            Instalacion.listaInstalaciones = db.instalaciones
            Torneo.torneos = db.torneos
            messagebox.showinfo("Cargar", "Datos cargados correctamente.")
        else:
            messagebox.showwarning("Cargar", "No se encontraron datos.")