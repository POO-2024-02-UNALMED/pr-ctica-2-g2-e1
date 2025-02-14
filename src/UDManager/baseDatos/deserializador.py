# src/UDManager/baseDatos/deserializador.py

import src.UDManager.gestorAplicacion.eventos.evento as ev
import src.UDManager.gestorAplicacion.inscripcion.grupoFormativo as gf
import src.UDManager.gestorAplicacion.pagos.cliente as cl
import src.UDManager.gestorAplicacion.reservas.reserva as res
import src.UDManager.gestorAplicacion.torneo.torneo as tor
import pickle

class Deserializador:
    @staticmethod
    def deserializar():
        try:
            with open("database.txt", "rb") as f:
                data = pickle.load(f)
                cl.Cliente.setListaClientes(data.get("clientes", []))
                res.Reserva.setListaReservas(data.get("reservas", []))
                tor.Torneo.setTorneos(data.get("torneos", []))
                gf.GrupoFormativo.setGrupoFormativos(data.get("grupoFormativos", []))
                ev.Evento.setEventos(data.get("eventos", []))
        except FileNotFoundError:
            print("No se encontró el archivo de base de datos.")
