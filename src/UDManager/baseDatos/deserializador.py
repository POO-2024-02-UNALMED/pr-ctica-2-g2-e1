# src/UDManager/baseDatos/deserializador.py

import src.UDManager.gestorAplicacion.eventos.evento as ev
import src.UDManager.gestorAplicacion.inscripcion.grupoFormativo as gf
import src.UDManager.gestorAplicacion.pagos.cliente as cl
import src.UDManager.gestorAplicacion.reservas.reserva as res
import src.UDManager.gestorAplicacion.reservas.instalacion as inst
import src.UDManager.gestorAplicacion.torneo.torneo as tor
from src.UDManager.gestorAplicacion.inscripcion.joven import Joven
import pickle
import os

class Deserializador:
    @staticmethod
    def deserializar():
        db_path = os.path.join(os.path.dirname(__file__), "..", "baseDatos", "database.txt")
        try:
            with open(db_path, "rb") as f:
                data = pickle.load(f)
                cl.Cliente.setListaClientes(data.get("clientes", []))
                res.Reserva.setListaReservas(data.get("reservas", []))
                inst.Instalacion.setListaInstalaciones(data.get("instalaciones", []))
                tor.Torneo.setTorneos(data.get("torneos", []))
                gf.GrupoFormativo.setGrupoFormativos(data.get("grupoFormativos", []))
                ev.Evento.setEventos(data.get("eventos", []))
                Joven.listaJovenes = data.get("jovenes", [])
        except (FileNotFoundError, EOFError):
            print("No se encontró el archivo de base de datos o está vacío. Se iniciará con datos por defecto.")
